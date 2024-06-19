import os
from copy import deepcopy
from os.path import dirname, realpath
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
from polaris.network.starts_logging import logger
from polaris.utils.database.database_dumper import EXCL_NAME_PAT
from polaris.utils.database.db_utils import list_tables_in_db, commit_and_close
from polaris.utils.database.standard_database import DatabaseType
from polaris.utils.model_checker import ModelChecker
from polaris.utils.optional_deps import check_dependency
from polaris.utils.signals import SIGNAL


class SupplyChecker(ModelChecker):
    """Network checker

    ::

        # We open the network
        from polaris.network.network import Network
        n = Network()
        n.open(source)

        # We get the checker for this network
        checker = n.checker

        # We can run the critical checks (those that would result in model crashing)
        checker.critical()

        # The active network connectivity
        checker.connectivity_walk()

        # The auto network connectivity
        checker.connectivity_auto()

        # The transit network connectivity
        checker.connectivity_transit()

        # The logic-based tests
        checker.run_algorithmic_tests()

        # Or simply run them all (with additional tests)
        checker.complete_analysis()
    """

    checking = SIGNAL(object)

    def __init__(self, path_to_file: os.PathLike):
        ModelChecker.__init__(self, DatabaseType.Supply, Path(dirname(realpath(__file__))), path_to_file)

        self._path_to_file = path_to_file
        self.logger = logger
        self.__networks: Optional[Any] = None

        self.walk_network_islands: Dict[int, List[int]] = {}
        self.transit_network_islands: Dict[int, List[int]] = {}
        self.auto_network_islands: Dict[int, List[int]] = {}
        self.checks_completed = 0
        self.errors: List[Any] = []
        self._network_file = path_to_file
        self._test_list.extend(
            [
                "consistency_tests",
                "deep_analysis",
                "connectivity_walk",
                "connectivity_auto",
                "connectivity_transit",
                "connections_table",
            ]
        )

    @property
    def networks(self):
        from polaris.network.checker.checks.connectivity_network import ConnectivityNetwork

        if self.__networks is None:
            self.__networks = ConnectivityNetwork(self._path_to_file)
        return self.__networks

    # TODO: Check if any Location or parking is affected by the islands
    def connectivity_walk(self) -> None:
        """Checks active network connectivity

        It computes paths between all nodes in the active network"""

        self._emit_start(1, "connectivity active")

        graph = self.networks.walk_graph
        if graph is None:
            return

        missing_walk_nodes = graph.all_nodes
        self.logger.info(f"     Analyzing active network connectivity for {graph.all_nodes.shape[0]} nodes")
        self.__compute_islands(graph, missing_walk_nodes, "active")
        self._emit_end("connectivity active")

    def has_critical_errors(self, fail_on_errors):
        self.critical()
        if len(self.errors) > 0:
            if fail_on_errors:
                self.logger.critical(self.errors)
                raise ValueError("YOUR SUPPLY FILE CONTAINS ERRORS")
            return True
        return False

    def connectivity_auto(self, turn_aware=True, high_memory_mode=False) -> None:
        """Checks auto network connectivity

        It computes paths between nodes in the network or between every single link/direction combination
        in the network

        Args:
             *turn_aware* (:obj:`Bool`): Indication of whether to run quick connectivity test or
             full turn-aware connectivity test. Defaults to True
             *high_memory_mode* (:obj:`Bool`): When true, checking uses **parallel** process which is
             faster, but uses more memory. Error logging for this option is not detailed
        """

        self._emit_start(1, "connectivity auto")

        graph = self.networks.auto_graph(turn_aware)
        if graph is None:
            return
        if turn_aware:
            self.__complete_path_search(graph, "auto", high_memory_mode)
        else:
            missing_auto_nodes = graph.all_nodes
            self.logger.info(f"     Analyzing auto network connectivity for {graph.all_nodes.shape[0]} nodes")
            self.__compute_islands(graph, missing_auto_nodes, "auto")
        self._emit_end("connectivity auto")

    def connectivity_transit(self) -> None:
        """Checks transit network connectivity

        It computes paths between transit stops using transit links and active links without
        considering temporal components of links
        """

        self._emit_start(1, "connectivity transit")
        graph = self.networks.transit_graph
        if graph is None:
            return

        missing_nodes = np.intersect1d(graph.all_nodes, np.array(self.networks.transit_stops)).tolist()
        self.logger.info(f"     Analyzing Transit network connectivity for {len(missing_nodes)} nodes")
        self.__compute_islands(graph, missing_nodes, "transit")
        self._emit_end("connectivity transit")

    def connections_table(self):
        """Includes
        * search for pockets that are not used in the connection table
        * search for pockets missing from the pockets table
        * search for lanes not connected to any other link at an intersection
        """

        self._emit_start(1, "connections table")
        from polaris.network.checker.checks.connection_table import CheckConnectionTable

        checker = CheckConnectionTable(self._path_to_file)
        checker.full_check()
        errors = checker.errors

        for key, val in errors.items():
            self.logger.error(key)
            self.logger.error(val)
        self._emit_end("connections table")

    def integer_test(self):
        """Tests if all tables in the standard are limit to int32 in size as to
        not break the Polaris reader"""
        from polaris.network.data.data_table_cache import DataTableCache

        dts = DataTableCache(self._network_file)
        dts.refresh_cache()
        with commit_and_close(self._path_to_file, spatial=True) as conn:
            all_tables = [tn for tn in list_tables_in_db(conn) if not any(x.match(tn) for x in EXCL_NAME_PAT)]

            for tbl in all_tables:
                df = dts.get_table(tbl, conn)
                if df.shape[0] == 0:
                    continue
                max_val = df.reset_index().max(skipna=True, numeric_only=True)
                if max_val.shape[0] == 0:
                    continue
                max_val = np.nanmax(max_val)
                if abs(max_val) > 2147483647:  # Maximum C++ value
                    m = f"Table {tbl} has numbers larger than the allowed integer"
                    self.errors.append(m)
                    self.logger.error(m)

    def deep_analysis(self):
        """Tests that search por possible inconsistencies in the network

        Includes

        * search for nodes connected to too many links (more than 4)
        """
        self._emit_start(1, "deep analysis")
        self.logger.info("\n    Nodes with too many connections")
        from polaris.network.checker.checks.busy_nodes import busy_nodes

        occurrences = busy_nodes(4, self._network_file)
        if occurrences:
            for key, val in occurrences.items():
                self._log_warn(f"Link {key} has {val} connections")
        else:
            self.logger.info("    None found")
        self._emit_end("deep analysis")

    def __complete_path_search(self, graph, mode: str, high_memory_mode):
        check_dependency("aequilibrae")
        from aequilibrae.paths.results import PathResults

        if mode != "auto":
            raise NotImplementedError("This is only implemented for autos")
        ncorresp = self.networks.auto_corresp

        if high_memory_mode:
            self.__complete_path_search_high_mem(graph, mode)
            return

        res = PathResults()
        res.prepare(graph)
        disconnections = {}
        tot = graph.all_nodes.shape[0]
        self.checking.emit(["start", "secondary", tot, self.master_message_name])
        tnode = graph.all_nodes[1]
        for i, fnode in enumerate(graph.all_nodes):
            self.checking.emit(["update", "secondary", i, self.master_message_name])
            res.compute_path(fnode, tnode)
            res.predecessors[graph.nodes_to_indices[fnode]] = 0
            missing_nodes = np.where(res.predecessors[:-1] < 0)[0]
            if missing_nodes.shape[0]:
                disconnections[fnode] = ncorresp[ncorresp.graph_node.isin(missing_nodes)].net_node.values
                self.logger.debug("Island found")
                self.logger.debug(list(missing_nodes))
            res.reset()
            tnode = fnode
        if not len(disconnections):
            self.logger.info(f"     Congratulations, your {mode} network is fully connected")
        else:
            tot = len(disconnections)
            self._log_warn(f"      Your {mode} network is disconnected. There are issues starting from {tot} links")
            self._log_warn(f"All disconnections: {disconnections}")
            self.errors.append(disconnections)

    def __complete_path_search_high_mem(self, graph, mode):
        check_dependency("aequilibrae")
        from aequilibrae import NetworkSkimming

        graph = deepcopy(graph)
        graph.prepare_graph(graph.all_nodes)
        graph.set_blocked_centroid_flows(False)
        graph.set_graph("distance")
        skm = NetworkSkimming(graph)
        skm.run()
        x = np.sum(skm.results.skims.distance)
        if np.isnan(x) or np.isinf(x):
            self.errors.append(f"There are disconnected links in the {mode} network")
            self._log_warn(f"      Your {mode} network is disconnected")

    def __compute_islands(self, graph, missing_nodes: np.ndarray, mode: str):
        check_dependency("aequilibrae")
        from aequilibrae.paths.results import PathResults

        if mode == "auto":
            self.auto_network_islands.clear()
            islands = self.auto_network_islands
            ncorresp = self.networks.auto_corresp
        elif mode == "transit":
            self.transit_network_islands.clear()
            islands = self.transit_network_islands
            ncorresp = self.networks.transit_corresp
        else:
            self.walk_network_islands.clear()
            islands = self.walk_network_islands
            ncorresp = self.networks.walk_corresp

        res = PathResults()
        res.prepare(graph)
        missing_nodes = np.array(missing_nodes)

        while missing_nodes.shape[0] >= 2:
            res.reset()
            res.compute_path(missing_nodes[0], missing_nodes[1])
            res.predecessors[graph.nodes_to_indices[missing_nodes[0]]] = 0
            connected = np.where(res.predecessors >= 0)
            connected = graph.all_nodes[connected]
            intersec_connected = np.intersect1d(missing_nodes, connected)  # type: np.ndarray
            missing_nodes = np.setdiff1d(missing_nodes, intersec_connected)

            isl = len(islands.keys())
            islands[isl] = list(intersec_connected)
            self.logger.debug("Island found")
            self.logger.debug(list(intersec_connected))

        isl = len(islands.keys())
        if len(missing_nodes) == 1:
            islands[isl] = list(missing_nodes)
            isl += 1

        if len(islands.keys()) == 1:
            self.logger.info(f"     Congratulations, your {mode} network is fully connected")
        else:
            max_nodes = max([len(nodes) for nodes in islands.values()])
            disc = graph.all_nodes.shape[0] - max_nodes
            self._log_warn(f"      Your {mode} network is disconnected. There are {isl} islands")
            self._log_warn(f"      There are {disc} nodes disconnected from the main {mode} network portion.")
            if len(islands.keys()):
                self._log_warn(f"        Found {len(islands.keys())} islands")
                all_nodes = []
                for val in islands.values():
                    if max_nodes > len(val):
                        all_nodes.extend(val)
                all_nodes = list(ncorresp[ncorresp.graph_node.isin(all_nodes)].net_node)
                self._log_warn(f"All disconnected: {str(set(all_nodes))}")
                self.errors.append(set(all_nodes))

    # This is required by QPolaris
    def _set_test_list(self, test_list):
        """Set the list of tests that constitute a complete analysis"""
        self._test_list = test_list
