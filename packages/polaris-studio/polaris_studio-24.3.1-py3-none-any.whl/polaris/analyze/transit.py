from pathlib import Path

from .transit_demand_metrics import DemandMetrics
from .transit_supply_metrics import SupplyMetrics


class Transit:
    """
    Parent class for all transit-related analysis. It should be accessed from :func:`~Polaris.analyze.Analyze`
    in the following way

    ::

            from Polaris import Polaris

            model = Polaris()
            model.open('path/to/model', 'config_file_name.json')
            analyze = model.analyze
            transit = analyze.transit()

            # For supply metrics

            sm = transit.supply_metrics
            boards_alights = sm.stop_metrics()
            supply_per_route_am = sm.route_metrics(from_minute=420, to_minute=540)
    """

    def __init__(self, supply_file: Path, demand_file: Path):
        self.__supply_file = supply_file
        self.__demand_file = demand_file

    def _set_demand_file(self, demand_file: Path) -> None:
        """Sets the demand file to be used for all transit analysis"""
        self.__demand_file = demand_file

    def _set_supply_file(self, supply_file: Path) -> None:
        """Sets the supply file to be used for all transit analysis"""
        self.__supply_file = supply_file

    def supply_metrics(self) -> SupplyMetrics:
        """Returns a class of :func:`~Polaris.analyze.transit_supply_metrics.SupplyMetrics`"""
        return SupplyMetrics(self.__supply_file)

    def demand_metrics(self) -> DemandMetrics:
        """Returns a class of :func:`~Polaris.analyze.transit_demand_metrics.DemandMetrics`"""
        return DemandMetrics(self.__supply_file, self.__demand_file)
