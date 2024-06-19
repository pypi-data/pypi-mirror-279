from pathlib import Path

from .tnc_metrics import TNCMetrics


class TNC:
    """Parent class for all tnc-related analysis. It should be accessed from :func:`~Polaris.analyze.Analyze`
        in the following way

    ::

            from Polaris import Polaris

            model = Polaris()
            model.open('path/to/model', 'config_file_name.json')
            analyze = model.analyze
            tnc = analyze.tnc()

            # For demand metrics

            dm = tnc.tnc_metrics
            wait_time_am = dm.wait_times(from_minute=420, to_minute=540)
    """

    def __init__(self, supply_file: Path, demand_file: Path, result_file: Path):
        self.__supply_file = supply_file
        self.__demand_file = demand_file
        self.__result_file = result_file

    def _set_demand_file(self, demand_file: Path) -> None:
        """Sets the demand file to be used for all tnc analysis"""
        self.__demand_file = demand_file

    def _set_supply_file(self, supply_file: Path) -> None:
        """Sets the supply file to be used for all tnc analysis"""
        self.__supply_file = supply_file

    def _set_result_file(self, result_file: Path) -> None:
        """Sets the result file to be used for all tnc analysis"""
        self.__result_file = result_file

    def tnc_metrics(self) -> TNCMetrics:
        """Returns a class of :func:`~Polaris.analyze.tnc_metrics.TNCMetrics`"""
        return TNCMetrics(self.__supply_file, self.__demand_file, self.__result_file)
