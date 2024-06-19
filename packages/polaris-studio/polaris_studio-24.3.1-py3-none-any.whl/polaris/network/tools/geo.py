import os
import sqlite3
import warnings
from math import atan2
from typing import Dict, Optional, Any, Union, List

import pandas as pd
import requests
import shapely.wkb
from polaris.network.active.bike_network_link import get_bike_links_qry
from polaris.network.active.walk_network_link import get_walk_links_qry
from polaris.network.data import data_table_cache
from polaris.network.database_connection import get_srid
from polaris.network.starts_logging import logger
from polaris.network.tools.geo_index import GeoIndex
from polaris.network.utils.geo_functions import compute_line_bearing
from polaris.utils.database.db_utils import commit_and_close, read_and_close
from polaris.utils.environment import inside_qgis
from polaris.utils.optional_deps import check_dependency
from shapely.geometry import Point, Polygon, LineString, MultiLineString, MultiPolygon
from shapely.ops import substring


class Geo:
    """Suite of generic geo-operations commonly used across other Polaris_Network submodules

    Changing the computation parameters is as simple as editing the dictionary **Geo.parameters**"""

    def __init__(self, network_file: os.PathLike):
        self.walk_link_idx = GeoIndex()
        self.bike_link_idx = GeoIndex()
        self.pt_routes_idx = GeoIndex()
        self.zone_idx = GeoIndex()
        self.walk_link_list: Dict[int, LineString] = {}
        self.bike_link_list: Dict[int, LineString] = {}
        self.zone_list: Dict[int, MultiPolygon] = {}
        self.pt_routes_list: Dict[int, MultiPolygon] = {}

        self.links: Dict[int, LineString] = {}
        self.link_idx = GeoIndex()
        self.mode_link_idx: Dict[str, GeoIndex] = {}
        self.geo_idx: Dict[str, GeoIndex] = {}
        self._outside_zones = 0
        self._far_walk_links = 0
        self._far_bike_links = 0
        self.graphs: Dict[str, Any] = {}
        self.__link_lanes: Dict[int, Any] = {}
        self.geo_objects: Dict[str, Any] = {}
        self.__model_area = None

        self.logger = logger
        self.map_matching: Dict[str, Union[int, float]] = {
            "links_to_search": 20,
            "bearing_tolerance": 22.5,
            "buffer_size": 32,
        }
        self._network_file = network_file
        self.__srid: Optional[int] = None
        self.__transformer: Optional[Any] = None
        self.__layers: Dict[str, Any] = {}

    @property
    def conn(self) -> int:
        raise Exception("NO CONNECTION HERE")

    @property
    def srid(self) -> int:
        if self.__srid is None:
            self.__srid = get_srid(database_path=self._network_file)
        return self.__srid

    @property
    def transformer(self):
        check_dependency("pyproj")
        from pyproj import Transformer

        if self.__transformer is None:
            self.__transformer = Transformer.from_crs(f"epsg:{self.srid}", "epsg:4326", always_xy=True)
        return self.__transformer

    def clear_cache(self) -> None:
        """Eliminates all data available on cache"""
        self.walk_link_idx.reset()
        self.walk_link_list.clear()
        self.bike_link_idx.reset()
        self.bike_link_list.clear()
        self.links.clear()
        self.link_idx.reset()
        self.mode_link_idx.clear()
        self.geo_idx.clear()
        self._outside_zones = 0
        self._far_walk_links = 0
        self._far_bike_links = 0
        self.graphs.clear()
        self.__link_lanes.clear()

    def get_timezone(self, conn: sqlite3.Connection):
        """Returns the time-zone for the current model. Uses the centroid of the model area as defined by the zoning
        layer"""
        poly = self.model_extent(conn)
        lon, lat = self.transformer.transform(poly.centroid.xy[0][0], poly.centroid.xy[1][0])

        url = f"http://api.geonames.org/timezoneJSON?formatted=true&lat={lat}&lng={lon}&username=pveigadecamargo"
        r = requests.get(url)
        return r.json()["timezoneId"]

    def model_extent(self, projection=None, conn: Optional[sqlite3.Connection] = None) -> Polygon:
        """Queries the extent of the zoning system included in the model

        Args:
            *projection* (:obj:`int` `Optional`): Projection for which to return the extent. Defaults to the
                                                  zone system's projection
        Returns:
            *model extent* (:obj:`Polygon`): Shapely polygon with the bounding box of the model zone system.
        """
        with conn or read_and_close(self._network_file, spatial=True) as conn:
            if projection is None:
                sql = 'Select ST_asBinary(GetLayerExtent("Zone"))'
            else:
                sql = f'Select ST_asBinary(ST_Transform(GetLayerExtent("Zone"), {projection})'
            return shapely.wkb.loads(conn.execute(sql).fetchone()[0])

    def get_zone(self, geometry: Union[Point, LineString, MultiLineString]) -> int:
        """Returns the zone in which a certain geometry is located.

            If the geometry is not fully enclosed by any zone, the zone that encloses the
            majority of the geometry is returned.  If the geometry does not overlap any zone, the closest is returned

            A debug message is raised if the closest zone is farther than 50km from the geometry

        Args:
            *geometry* (:obj:`Point` or :obj:`LineString`): A Shapely geometry object

        Return:
            *zone* (:obj:`int`): ID of the zone applicable to the point provided
        """

        self.__build_zone_idx()
        nearest = list(self.zone_idx.nearest(geometry, 10))
        dists = []
        for near in nearest:
            if self.zone_list[near].contains(geometry):
                return near
            dists.append(self.zone_list[near].distance(geometry))

        if not dists:
            return -1
        near = min(dists)
        return nearest[dists.index(near)]

    def get_pt_routes(self, geometry: Union[Point, LineString, MultiLineString, Polygon, MultiPolygon]) -> List[int]:
        """Returns all route_ids for all routes that intersect the input geometry.
           Not available for the QGIS interface

        Args:
            *geometry* (:obj:`Point` or :obj:`LineString`): A Shapely geometry object

        Return:
            *zone_ids* (:obj:`List[int]`): List of route_id
        """

        self.__build_pt_routes_idx()
        candidates = self.pt_routes_idx.idx.intersection(geometry.bounds)
        return [c for c in candidates if self.pt_routes_list[c].intersects(geometry)]

    def get_walk_link(self, point: Point, precision=100) -> int:
        """Get the PHYSICAL walk link closest to the point provided.

            By physical link, it is meant a link with a valid ref_link value in the Link table.

            A spatial index check is performed to narrow down the number of candidates for actual
            distance computation. Bigger numbers ensure precision, but at a high computational cost.
            Parameters between 10 and 20 have proved ideal and nearly 100% precise.

            A warning is raised if the closest link is farther than 2km from the Point if in debug mode

        Args:
            *point* (:obj:`Point`): A Shapely Point object
            *precision* (:obj:`int`): Number of links to retrieve from spatial index for distance computation

        Return:
            *walk_link* (:obj:`int`): ID of the walk_link closest to the point provided
        """

        # sql2 = '''select walk_link, distance(geo, GeomFromWKB(?, ?)) d from Transit_Walk order by d limit 1'''
        # self.__curr.execute(sql2, [point.wkb, self.srid])
        # dt = self.__curr.fetchone()
        # if not dt:
        #     return None
        # return dt[0]

        if not self.walk_link_idx.built:
            self.__build_walk_links_index()

        nearest = list(self.walk_link_idx.nearest(point, precision))
        if not nearest:
            return -1
        distances = [point.distance(self.walk_link_list[x]) for x in nearest]
        close = nearest[distances.index(min(distances))]
        if min(distances) > 2000:
            self._far_walk_links += 1
        return close

    def get_any_link(self, point: Point, precision=20) -> int:
        """Get the link from the network closest to the point provided.

            A spatial index check is performed to narrow down the number of candidates for actual
            distance computation. Bigger numbers ensure precision, but at a high computational cost.
            Parameters between 10 and 20 have proved ideal and nearly 100% precise.

            A warning is raised if the closest link is farther than 2km from the Point if in debug mode

        Args:
            *point* (:obj:`Point`): A Shapely Point object
            *precision* (:obj:`int`): Number of links to retrieve from spatial index for distance computation

        Return:
            *link* (:obj:`int`): ID of the link closest to the point provided
        """

        # sql2 = '''select walk_link, distance(geo, GeomFromWKB(?, ?)) d from Transit_Walk order by d limit 1'''
        # self.__curr.execute(sql2, [point.wkb, self.srid])
        # dt = self.__curr.fetchone()
        # if not dt:
        #     return None
        # return dt[0]

        self.build_mode_link_index("")
        self.link_idx = self.mode_link_idx[self._mode_name("")]

        nearest = list(self.link_idx.nearest(point, precision))
        if not nearest:
            return -1
        distances = [point.distance(self.links[x]) for x in nearest]
        return nearest[distances.index(min(distances))]

    def get_bike_link(self, point: Point, precision=100) -> Optional[int]:
        """Get the PHYSICAL bike link closest to the point provided.

            By physical link, it is meant a link with a valid ref_link value in the Link table.

            A spatial index check is performed to narrow down the number of candidates for actual
            distance computation. Bigger numbers ensure precision, but at a high computational cost.
            Parameters between 10 and 20 have proved ideal and nearly 100% precise.

            A warning is raised if the closest link is farther than 2km from the Point if in debug mode

        Args:
            *point* (:obj:`Point`): A Shapely Point object
            *precision* (:obj:`int`): Number of links to retrieve from spatial index for distance computation

        Return:
            *bike_link* (:obj:`int`): ID of the bike_link closest to the point provided
        """

        # sql2 = '''select walk_link, distance(geo, GeomFromWKB(?, ?)) d from Transit_Walk order by d limit 1'''
        # self.__curr.execute(sql2, [point.wkb, self.srid])
        # dt = self.__curr.fetchone()
        # if not dt:
        #     return None
        # return dt[0]

        if not self.bike_link_idx.built:
            self.__build_bike_links_index()

        nearest = list(self.bike_link_idx.nearest(point, precision))
        if not nearest:
            return None
        distances = [point.distance(self.bike_link_list[x]) for x in nearest]
        close = nearest[distances.index(min(distances))]
        if min(distances) > 2000:
            self._far_bike_links += 1
        return close

    def get_locations(self, point: Point, elements=1) -> List[int]:
        """Get the list of Locations within a certain distance from the point

        Args:
            *point* (:obj:`Point`): A Shapely Point object
            *elements* (:obj:`int`): Number of locations to return

        Return:
            *locations* (:obj:`List[int]`): List of location IDs
        """
        lyr = "location"
        idx = self.geo_idx.get(lyr, None)
        if idx is None:
            if inside_qgis:
                idx = GeoIndex()
                self.geo_objects[lyr] = idx.build_from_layer(self.__layers[lyr])
            else:
                idx = self.build_index_from_table("Location")
            self.geo_idx[lyr] = idx

        return list(idx.nearest(point, elements))

    def get_parkings(self, point: Point, maximum_parking_distance: float) -> List[int]:
        """Get the list of Parking facilities within a certain distance from the point

        Args:
            *point* (:obj:`Point`): A Shapely Point object
            *maximum_parking_distance* (:obj:`int`): Maximum distance for a certain parking_id

        Return:
            *parkings* (:obj:`List[int]`): List of Parking IDs
        """
        lyr = "parking"
        idx = self.geo_idx.get(lyr, None)
        if idx is None:
            if inside_qgis:
                idx = GeoIndex()
                self.geo_objects[lyr] = idx.build_from_layer(self.__layers[lyr])
            else:
                idx = self.build_index_from_table("Parking")
            self.geo_idx[lyr] = idx

        nearest = idx.nearest(point, 100)
        return [x for x in nearest if self.geo_objects[lyr][x].distance(point) < maximum_parking_distance]

    def get_link_overlap(self, link: LineString) -> list:
        """Analyzes the network in search of any links overlapping a given LineString segment

        Args:

            *link* (:obj:`LineString`): Segment for which we want to find corresponding links in the network

        Returns:

            *overlap_length* (:obj:`float`): The overlapping link length found in the network
            *link_list* (:obj:`List[int]`): The list of links with positive overlap with our segment
        """

        buffer_size = self.map_matching["buffer_size"]
        bearing_tolerance = self.map_matching["bearing_tolerance"]
        links_to_search = self.map_matching["links_to_search"]

        self.build_mode_link_index("")
        self.link_idx = self.mode_link_idx[self._mode_name("")]
        buffer = link.buffer(buffer_size)
        nearest = list(self.link_idx.nearest(buffer, links_to_search))
        return_length = 0.0
        list_links = []
        line_bearing = compute_line_bearing(link.coords[0], link.coords[-1])
        for x in nearest:
            candidate = self.links[x]
            with warnings.catch_warnings():
                # ignore a spurious class of warning from geos: https://github.com/libgeos/geos/issues/515
                warnings.filterwarnings(action="ignore", message="invalid value encountered")
                all_inter = buffer.intersection(candidate)
            if all_inter:
                all_inter = list(all_inter.geoms) if isinstance(all_inter, MultiLineString) else [all_inter]
                for intersection in all_inter:
                    intersec_bearing = compute_line_bearing(intersection.coords[0], intersection.coords[-1])
                    if abs(intersec_bearing - line_bearing) < bearing_tolerance:
                        return_length += intersection.length
                        list_links.append(x)
        return [return_length, set(list_links)]

    def get_link_overlap_by_mode(self, link: LineString, mode: Union[str, list]) -> list:
        """Analyzes the network in search of links (of an specific mode) overlapping a given LineString segment

        All components from the map_matching parameter dictionary are used:

        * **links_to_search**: Number of link candidates to retrieve from the spatial index analysis
        * **bearing_tolerance**: Line bearing difference to consider links compatible with each other
        * **buffer_size**: Buffer size (meters) for link search

        Args:

            *link* (:obj:`LineString`): Segment for which we want to find corresponding links in the network
            *mode* (:obj:`str`): Mode to consider when searching

        Returns:

            *overlap_length* (:obj:`float`): The overlapping link length found in the network
            *link_list* (:obj:`List[int]`): The list of links with positive overlap with our segment
        """

        # parameters
        buffer_size = self.map_matching["buffer_size"]
        bearing_tolerance = self.map_matching["bearing_tolerance"]
        links_to_search = self.map_matching["links_to_search"]

        # Will be used to compute the overlap between the segment in question and
        # each corresponding link in the network
        start_point = link.boundary.geoms[0]
        end_point = link.boundary.geoms[-1]

        modename = self._mode_name(mode)
        self.build_mode_link_index(mode)

        idx = self.mode_link_idx[modename]
        buffer = link.buffer(buffer_size)
        nearest = list(idx.nearest(buffer, links_to_search))
        return_length = 0.0
        list_links = []
        line_bearing = compute_line_bearing(link.coords[0], link.coords[-1])
        for x in nearest:
            candidate = self.links[x]

            with warnings.catch_warnings():
                # ignore a spurious class of warning from geos: https://github.com/libgeos/geos/issues/515
                warnings.filterwarnings(action="ignore", message="invalid value encountered")
                all_inter = buffer.intersection(candidate)

            if all_inter:
                all_inter = list(all_inter.geoms) if isinstance(all_inter, MultiLineString) else [all_inter]
                for intersection in all_inter:
                    if intersection.length > 0:
                        fpos = intersection.project(start_point)
                        tpos = intersection.project(end_point)
                        seg = substring(intersection, fpos, tpos)
                        if seg.length > 0:
                            intersec_bearing = compute_line_bearing(seg.coords[0], seg.coords[-1])
                            if abs(intersec_bearing - line_bearing) < bearing_tolerance:
                                return_length += seg.length
                                list_links.append(x)
        return [return_length, list(set(list_links))]

    def get_links_for_point(self, point: Point, max_distance=0):
        """Analyzes the network in search of links (of an specific mode) closest to a given point. It no link is found,
        the closest link is returned
        Args:
            *point* (:obj:`Point`): Point for which we want to find closest link in the network
            *max_distance* (:obj:`float`): Maximum distance to return any result
        """

        # parameters
        check_dependency("geopandas")
        import geopandas as gpd

        llayer = self.get_layer("link")
        data = gpd.GeoDataFrame({"geometry": [point]}, crs=self.srid)
        layer = llayer.sjoin_nearest(data, max_distance=max_distance, distance_col="distance")
        return layer[["link", "use_codes", "distance", "geo"]].sort_values("distance").reset_index(drop=True)

    def get_link_for_point_by_mode(self, point: Point, mode: Union[str, list], results=1, max_distance=0) -> List[int]:
        """Analyzes the network in search of links (of an specific mode) closest to a given point

        The number of link candidates to retrieve from the spatial index analysis is defined by the
        parameter *links_to_search* in the map_matching parameter dictionary.

        Args:

            *point* (:obj:`Point`): Point for which we want to find closest link in the network
            *mode* (:obj:`str` or :obj:`list`): Mode (or modes) to consider when searching. When a list of modes is
                                                is provided, only links that allow ALL modes are considered
            *max_distance* (:obj:`float`): Maximum distance to return any result. Minimum number of results is 1. If
                                           zero, no distance threshold is imposed

        Returns:

            *list* (:obj:`List[int]`): List of link IDs found near point geometry
        """

        # parameters
        links_to_search = self.map_matching["links_to_search"]
        modename = self._mode_name(mode)

        if modename not in self.mode_link_idx:
            self.build_mode_link_index(mode)
        idx = self.mode_link_idx[modename]

        nearest = list(idx.nearest(point, links_to_search))
        if not nearest:
            return []
        distances = [point.distance(self.links[x]) for x in nearest]

        df = pd.DataFrame({"link": nearest, "distance": distances}).sort_values(by="distance")
        if max_distance > 0:
            df = df[df.distance <= max_distance]

        if results >= df.shape[0]:
            return df.link.tolist()
        return df.link.tolist()[:results]

    def offset_for_point_on_link(self, link: int, point: Point, conn: Optional[sqlite3.Connection] = None) -> float:
        """
            Given a link ID and a Point, this method computes the offset of point

            It takes flow directionality (ab/ba lanes) in consideration when computing if the link
            will be accessed in one direction or another

        Args:

            *link* (:obj:`int`): Link ID to compute offset for
            *point* (:obj:`Point`): Point object to compute offset for

        Returns
            *offset* (:obj:`float`): Distance along a link a node is located in
        """

        self.build_mode_link_index("")
        self.link_idx = self.mode_link_idx[self._mode_name("")]

        with conn or read_and_close(self._network_file) as conn:
            if not self.__link_lanes:
                for x in conn.execute("Select link, lanes_ab, lanes_ba from Link").fetchall():
                    self.__link_lanes[x[0]] = x[1:]

        link_geo = self.links[link]
        tot_len = link_geo.length
        projected = link_geo.project(point)
        cap = self.__link_lanes[link]

        if cap[0] == 0:
            ofst = tot_len - projected
        elif cap[1] == 0:
            ofst = projected
        else:
            proj_node = link_geo.interpolate(projected)
            az1 = self.azimuth(proj_node, point)
            next_node = link_geo.interpolate(projected + 0.1 * (tot_len - projected))
            az2 = self.azimuth(proj_node, next_node)
            ofst = projected if az1 - az2 > 0 else tot_len - projected

        return round(ofst, 8)

    def offset_for_point_on_walk_link(
        self, walk_link: int, point: Point, conn: Optional[sqlite3.Connection] = None
    ) -> float:
        """
            Given a WALK link ID and a Point, this method computes the offset of point


        Args:

            *link* (:obj:`int`): WALK Link ID to compute offset for
            *point* (:obj:`Point`): Point object to compute offset for

        Returns
            *offset* (:obj:`float`): Distance along the active link a node is located in
        """

        sql = (
            'select round(ST_Line_Locate_Point(geo, GeomFromWKB(?,?)) * "length", 8) from Transit_Walk '
            "where walk_link=? limit 1"
        )
        with conn or read_and_close(self._network_file, spatial=True) as conn:
            dt = conn.execute(sql, [point.wkb, self.srid, walk_link]).fetchone()
        if not dt:
            return -1
        return dt[0]

    def side_of_link_for_point(self, point: Point, link: Union[int, LineString]) -> int:
        """Computes the side of the link a point is with relationship to a line

        Args:

            *link* (:obj:`int`): Link ID of the link in question
            *point* (:obj:`Point`): Geometry of the point we are interested in
            *link_geo* (:obj:`LineString`): Geometry of the link we want to find the side for. **Optional**

        Returns
            *side* (:obj:`int`): 0 for right side and 1 for left

        """
        lgeo = self.links[link] if isinstance(link, int) else link
        tot_len = lgeo.length
        offset = lgeo.project(point)
        projected = lgeo.interpolate(offset)  # type: Point
        other_proj = min(tot_len / 2, 1) if offset == 0 else max(0, offset - 1)
        other_point = lgeo.interpolate(other_proj)  # type: Point

        fpoint = projected if other_proj < offset else other_point
        tpoint = projected if other_proj > offset else other_point

        side = (point.x - fpoint.x) * (tpoint.y - fpoint.y) - (point.y - fpoint.y) * (tpoint.x - fpoint.x)
        return 0 if side <= 0 else 1

    def _mode_name(self, mode: Union[list, str]) -> str:
        if isinstance(mode, str):
            return mode
        return "|".join(mode)

    def get_mode_link_index(self, mode: Union[list, str]) -> GeoIndex:
        """Gets the spatial index for links for a certain mode. If not ready, builds it

        Args:
            *mode* (:obj:`str` or `List[str]`): Mode or modes to be considered in combination
        """

        modename = self._mode_name(mode)
        self.build_mode_link_index(mode)
        return self.mode_link_idx[modename]

    def build_mode_link_index(self, mode: Union[list, str]):
        """Build the spatial index for links for a certain mode

        Args:

            *mode* (:obj:`str` or `List[str]`): Mode or modes to be considered in combination
        """
        if self._mode_name(mode) in self.mode_link_idx:
            return
        get_qry = "Select link, asbinary(geo) from Link"
        if len(mode):
            get_qry += " INNER JOIN Link_Type ON Link.type = Link_Type.link_type"
            if isinstance(mode, str):
                get_qry += f' WHERE INSTR(Link_Type.use_codes, "{mode}")>0'
            else:
                sel_str = " AND ".join([f'INSTR(Link_Type.use_codes, "{m}")>0' for m in mode])
                get_qry += f" WHERE {sel_str}"

        idx = GeoIndex()
        self.logger.debug("  Reading roadway links and building spatial index")

        with commit_and_close(self._network_file, spatial=True) as conn:
            for link, wkb in conn.execute(get_qry).fetchall():
                self.links[link] = shapely.wkb.loads(wkb)  # The link dictionary can be a single one for all modes
                idx.insert(feature_id=link, geometry=self.links[link])

        self.mode_link_idx[self._mode_name(mode)] = idx

    def build_index_from_table(self, table_name: str) -> GeoIndex:
        tn = table_name.lower()
        self.geo_objects[tn] = {}
        self.logger.debug(f"   Building {table_name} index")
        tables = data_table_cache.DataTableCache(self._network_file)
        df = tables.get_table(table_name)
        idx = GeoIndex()
        # We build the spatial index with the locations
        for ind, record in df.iterrows():  # type: ignore
            geo = shapely.wkb.loads(record.geo)
            idx.insert(feature_id=ind, geometry=geo)  # type: ignore
            self.geo_objects[tn][ind] = geo
        return idx

    @property
    def modeling_area(self):
        """Returns the modelling are as the union of all zones as a single MultiPolygon"""
        return self.__model_area or self.__build_modelling_area()

    def __build_modelling_area(self):
        with read_and_close(self._network_file, spatial=True) as conn:
            wkb = conn.execute("select AsBinary(ST_Union(geo)) from zone").fetchone()[0]
        self.__model_area = shapely.wkb.loads(wkb)
        return self.__model_area

    def __build_walk_links_index(self) -> None:
        # We build the spatial index with the walk links

        self.logger.debug("   Building walk links index")
        self.walk_link_idx, self.walk_link_list = self.__build_index_from_qry(get_walk_links_qry)

    def __build_bike_links_index(self) -> None:
        # We build the spatial index with the bike links
        self.logger.debug("   Building bike links index")
        self.bike_link_idx, self.bike_link_list = self.__build_index_from_qry(get_bike_links_qry)

    def __build_index_from_qry(self, qry):
        with read_and_close(self._network_file, spatial=True) as conn:
            idx = GeoIndex()
            feature_list = {}
            for record in conn.execute(qry).fetchall():
                obj_id = record[0]
                geo = shapely.wkb.loads(record[-1])
                feature_list[obj_id] = geo
                idx.insert(feature_id=obj_id, geometry=geo)
        return idx, feature_list

    def __build_zone_idx(self):
        if self.zone_idx.built:
            return

        self.logger.debug("   Building zone index")
        qry = "Select zone, asbinary(geo) from Zone where geo is not Null"
        self.zone_idx, self.zone_list = self.__build_index_from_qry(qry)

    def __build_pt_routes_idx(self):
        if self.pt_routes_idx.built:
            return

        self.logger.debug("   Building zone index")
        qry = "Select route_id, asbinary(geo) from Transit_Routes where geo is not Null"
        self.pt_routes_idx, self.pt_routes_list = self.__build_index_from_qry(qry)

    def _set_srid(self, srid: int) -> None:
        self.__srid = srid

    def azimuth(self, point1, point2) -> float:
        """Returns the azimuth between two points

        Args:
            *point1* (:obj:`Point`): A Shapely point object
            *point2* (:obj:`Point`): A Shapely point object
        """
        return atan2(point2.x - point1.x, point2.y - point1.y)

    def clear_layers(self):
        self.__layers.clear()

    def get_layer(self, layer_name: str):
        if layer_name not in self.__layers:
            with commit_and_close(self._network_file, spatial=True) as conn:
                layer = data_table_cache.DataTableCache(self._network_file).get_geo_layer(layer_name, conn)
                if layer_name.lower() == "link":
                    lt = data_table_cache.DataTableCache(self._network_file).get_table("Link_type")
                    layer = layer.merge(lt, left_on="type", right_on="link_type", how="left")
            self.__layers[layer_name] = layer
        return self.__layers[layer_name]

    def add_layer(self, layer, layer_name: str):
        # This function is needed for QPolaris
        self.__layers[layer_name] = layer
