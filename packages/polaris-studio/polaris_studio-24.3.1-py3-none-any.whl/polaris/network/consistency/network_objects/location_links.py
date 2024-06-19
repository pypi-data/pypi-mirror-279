import logging

import geopandas as gpd
import numpy as np
import pandas as pd


def location_links_builder(lnks: gpd.GeoDataFrame):
    # First we will create the main direction for each location

    # We only need one record per location, so we get the closest link for each location that
    # allows for both cars and pedestrians and the closest link that allow cars if no link allows for both
    closest_both = lnks[(lnks.is_auto) & (lnks.is_walk)]
    closest_cars = lnks[lnks.is_auto & (~lnks.location.isin(closest_both.location))]
    closest = pd.concat([closest_both, closest_cars])
    closest = closest.sort_values("distance").drop_duplicates("location").reset_index(drop=True)

    # We get the closest link and its projection and return the projection point
    logging.getLogger("polaris").debug("Location_Links - Getting projection points")
    vectors = closest.loc_geo.shortest_line(closest.geometry)
    coords = vectors.get_coordinates()
    coords = coords[coords.index.duplicated(keep="first")]

    prj_p = gpd.GeoSeries.from_xy(coords["x"], coords["y"], crs=closest.crs)

    # We will now compute the vector connecting each location to its closest link
    # and rotate it by 45 degrees to get a proper coverage around the location
    alpha_ = np.arctan2(prj_p.y - closest.loc_geo.y, prj_p.x - closest.loc_geo.x)
    x_ = closest.loc_geo.x
    y_ = closest.loc_geo.y

    # The closest link will always be included
    loc_links = [closest[["location", "link"]]]

    # Now we loop through all angles at 45 degree intervals to get all surrounding links
    for rot in range(45, 360, 45):
        logging.getLogger("polaris").debug(f"Location_Links - Rotating vector by {rot} degrees")
        alpha = alpha_ + np.radians(rot)
        x = x_ + closest.dist_thresh * np.cos(alpha)
        y = y_ + +closest.dist_thresh * np.sin(alpha)
        prj_p = gpd.GeoSeries.from_xy(x, y, crs=closest.crs)
        vector = closest.loc_geo.shortest_line(prj_p)
        # Bring the vector to the location link dataframe
        gdf = lnks.merge(pd.DataFrame({"location": closest.location, "vec_geo": vector}), on="location", how="inner")
        gdf = gdf[gdf.geometry.intersects(gdf.vec_geo)]

        # We update the distance to be the distance from the location to the link that THAT SPECIFIC direction
        gdf.distance = gdf.loc_geo.distance(gdf.vec_geo.intersection(gdf.geometry))
        gdf = gdf.sort_values("distance").drop_duplicates("location")
        loc_links.append(gdf[["location", "link"]])

    # There are rare cases where the candidates are just at the limit of the distance threshold
    # Abd imprecision, as well
    return pd.concat(loc_links).drop_duplicates(ignore_index=True)


def build_on_df(df: pd.DataFrame) -> pd.DataFrame:
    # Only walk and auto would be used later, so let's keep it
    df = df.assign(is_auto=df.use_codes.str.contains("AUTO"), is_walk=df.use_codes.str.contains("WALK"))
    # We classify each link as whether walk is allowed or not
    return df[df.is_auto & df.is_walk]


def loc_link_candidates(locs, links_layer, distance_threshold):
    # We search all link candidates for all locations at once
    # This is MUCH faster than going blind for each location
    dt = distance_threshold

    all_loc_links = []
    locs = locs.rename_geometry("loc_geo")
    while locs.shape[0] > 0 and dt < 50000:
        loc_buff = gpd.GeoDataFrame(locs[["location"]], geometry=locs.buffer(dt), crs=locs.crs)
        loc_links = links_layer.sjoin(loc_buff, how="inner", predicate="intersects")
        loc_links = loc_links.merge(locs[["location", "loc_geo"]], on="location")
        loc_links = loc_links.assign(distance=loc_links.geometry.distance(loc_links.loc_geo))
        loc_links = build_on_df(loc_links).assign(dist_thresh=dt)
        locs = locs[~locs.location.isin(loc_links.location)]
        dt *= 1.2
        all_loc_links.append(loc_links)

    return pd.concat(all_loc_links) if all_loc_links else pd.DataFrame(columns=["location", "link"])
