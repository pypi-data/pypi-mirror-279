from os import PathLike
from typing import Any, Dict

import numpy as np
import pandas as pd

from polaris.network.constants import WALK_AGENCY_ID
from polaris.network.starts_logging import logger
from polaris.utils.database.db_utils import commit_and_close
from polaris.utils.optional_deps import check_dependency


class ConnectivityNetwork:
    def __init__(self, database_path: PathLike):
        self.__graphs: Dict[str, Any] = {}
        self.logger = logger
        self.__walk_net = pd.DataFrame([])
        self.__transit_net = pd.DataFrame([])
        self.__transit_stops = None
        self.__database_path = database_path

    def auto_graph(self, turnaware=False):
        mode = "auto_connections" if turnaware else "auto"
        if mode in self.__graphs:
            return self.__graphs[mode]

        self.__graphs[mode] = None
        auto_net = self.__get_auto_net(turnaware)

        if auto_net is not None:
            logger.debug(f"       Auto network has {auto_net.shape[0]} total links")
            self.__graphs[mode] = self.__set_graph(auto_net)
            logger.debug(f"       Transit graph has {self.__graphs[mode].graph.shape[0]} UNIdirectional links")

        return self.__graphs[mode]

    @property
    def transit_graph(self):
        if "transit" in self.__graphs:
            return self.__graphs["transit"]
        self.__graphs["transit"] = None
        logger.debug("    Building Transit Network")
        tn = self.transit_net

        if not tn.shape[0]:
            return
        logger.debug(f"       Transit network has {tn.shape[0]} UNIdirectional links")

        net = pd.concat([pd.DataFrame(self.walk_net), pd.DataFrame(tn)])
        net = net[["old_link", "direction", "fnode", "tnode", "distance"]]
        net = self.__indexes_networks(net)

        self.__graphs["transit"] = self.__set_graph(net)
        logger.debug(f'       Transit graph has {self.__graphs["transit"].graph.shape[0]} UNIdirectional links')
        return self.__graphs["transit"]

    @property
    def walk_graph(self):
        if "active" in self.__graphs:
            return self.__graphs["active"]
        self.__graphs["active"] = None
        logger.debug("    Building walking Network")
        wn = self.walk_net
        self.__graphs["active"] = self.__set_graph(wn)
        logger.debug(f"       Walk network has {wn.shape[0]} BIdirectional links")
        logger.debug(f'       Walk graph has {self.__graphs["active"].graph.shape[0]} UNIdirectional links')
        return self.__graphs["active"]

    @property
    def transit_stops(self):
        if self.__transit_stops is not None:
            return self.__transit_stops

        get_qry = f"Select stop_id from Transit_Stops where agency_id != {WALK_AGENCY_ID}"
        with commit_and_close(self.__database_path, commit=False) as conn:
            stops = pd.read_sql(get_qry, conn).stop_id
        _ = self.transit_net
        stops = self.transit_corresp[self.transit_corresp.net_node.isin(stops)]
        self.__transit_stops = list(stops.graph_node.values)
        return self.__transit_stops

    @property
    def walk_net(self):
        if self.__walk_net.shape[0] > 0:
            return self.__walk_net
        get_qry = 'Select walk_link old_link, from_node fnode, to_node tnode, "length" distance from Transit_Walk'
        with commit_and_close(self.__database_path, commit=False) as conn:
            records = pd.read_sql(get_qry, conn)
        records = records.assign(direction=0)

        records = records[["old_link", "direction", "fnode", "tnode", "distance"]]
        self.__walk_net = pd.DataFrame([])
        if records.shape[0]:
            records = self.__indexes_networks(records)
            self.walk_corresp = self.__build_node_corresp(records)
            self.__walk_net = pd.DataFrame(records)
        return self.__walk_net

    @property
    def transit_net(self) -> pd.DataFrame:
        if self.__transit_net.shape[0] > 0:
            return self.__transit_net
        get_qry = 'Select transit_link old_link, from_node fnode, to_node tnode, "length" distance from Transit_Links'
        with commit_and_close(self.__database_path, commit=False) as conn:
            records = pd.read_sql(get_qry, conn)
        records = records.assign(direction=0)

        records = records[["old_link", "direction", "fnode", "tnode", "distance"]]
        self.__transit_net = pd.DataFrame([])
        if records.shape[0]:
            records = self.__indexes_networks(records)
            self.transit_corresp = self.__build_node_corresp(records)
            self.__transit_net = pd.DataFrame(records)
        return self.__transit_net

    def __get_auto_net(self, turnaware=False) -> pd.DataFrame:
        get_qry = """SELECT link old_link, 0 direction, Node_a fnode, Node_b tnode, "length" distance from Link
                             INNER JOIN Link_Type ON Link.type = Link_Type.link_type
                             WHERE lanes_ab> 0 AND lanes_ba> 0 AND INSTR(Link_Type.use_codes, 'AUTO')>0
                     UNION ALL
                     SELECT link old_link, 1 direction, Node_a fnode, Node_b tnode, "length" distance from Link
                             INNER JOIN Link_Type ON Link.type = Link_Type.link_type
                             WHERE lanes_ab> 0 AND lanes_ba= 0 AND INSTR(Link_Type.use_codes, 'AUTO')>0
                     UNION ALL
                     SELECT link old_link, 1 direction, Node_b fnode, Node_a tnode, "length" distance from Link
                             INNER JOIN Link_Type ON Link.type = Link_Type.link_type
                             WHERE lanes_ab= 0 AND lanes_ba> 0 AND INSTR(Link_Type.use_codes, 'AUTO')>0"""

        if turnaware:
            get_qry = "SELECT conn old_link, 1 direction,  2 * link + dir fnode, 2 * to_link + to_dir tnode, 1 distance from Connection"
        with commit_and_close(self.__database_path, commit=False) as conn:
            records = pd.read_sql(get_qry, conn)
        records = records[["old_link", "direction", "fnode", "tnode", "distance"]]
        if not records.shape[0]:
            return pd.DataFrame([])
        records = self.__indexes_networks(records)
        self.auto_corresp = self.__build_node_corresp(records)
        return pd.DataFrame(records)

    def __indexes_networks(self, records):
        nodes = np.sort(np.unique(np.hstack([records.fnode.values, records.tnode.values])))
        corresp = pd.DataFrame({"fnode": nodes, "a_node": np.arange(nodes.shape[0]) + 1})
        links = np.sort(np.unique(records.old_link))
        link_corresp = pd.DataFrame({"old_link": links, "link_id": np.arange(links.shape[0]) + 1})

        records = records.merge(corresp, on="fnode")
        corresp.columns = ["tnode", "b_node"]
        records = records.merge(corresp, on="tnode")
        records = records.merge(link_corresp, on="old_link")
        return records

    def __build_node_corresp(self, records):
        net = pd.DataFrame(records)
        df1 = net[["a_node", "fnode"]]
        df1.columns = ["graph_node", "net_node"]
        df2 = net[["b_node", "tnode"]]
        df2.columns = ["graph_node", "net_node"]
        df2 = pd.concat([df1, df2])
        return df2.drop_duplicates()

    def __set_graph(self, net: pd.DataFrame):
        check_dependency("aequilibrae")
        from aequilibrae import Graph

        centroids = np.unique(np.vstack([net["a_node"], net["b_node"]]))

        graph = Graph()
        graph.network_ok = True
        graph.status = "OK"
        graph.network = net
        graph.prepare_graph(centroids)
        graph.set_blocked_centroid_flows(False)
        graph.mode = "c"
        graph.set_graph("distance")
        graph.set_skimming(["distance"])
        return graph
