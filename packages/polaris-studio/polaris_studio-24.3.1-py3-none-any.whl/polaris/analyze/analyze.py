import os
from pathlib import Path
from typing import Optional

from .tnc import TNC
from .transit import Transit


class Analyze:
    """Analysis submodule

    ::

        from Polaris import Polaris

        model = Polaris()
        model.open('path/to/model', 'config_file_name.json')
        analyze = model.analyze()
    """

    def __init__(self, supply_file: Path, demand_file: Path, result_file: Path):
        self.__transit: Optional[Transit] = None
        self.__tnc: Optional[TNC] = None
        self.__supply_file = Path(supply_file)
        self.__demand_file = Path(demand_file)
        self.__result_file = Path(result_file)

    def transit(self):
        """Returns a class of :func:`~Polaris.analyze.transit.Transit`"""
        if self.__transit is None:
            self.__transit = Transit(self.__supply_file, self.__demand_file)
        return self.__transit

    def tnc(self):
        """Returns a class of :func:`~Polaris.analyze.tnc.TNC`"""
        if self.__tnc is None:
            self.__tnc = TNC(self.__supply_file, self.__demand_file, self.__result_file)
        return self.__tnc

    def set_demand_file(self, demand_file: Path):
        """

        :param supply_file:
        :return:
        """
        self.__demand_file = demand_file
        if self.__transit is not None:
            self.__transit._set_demand_file(demand_file)

    def set_supply_file(self, supply_file: Path):
        """

        :param supply_file:
        :return:
        """
        if not supply_file.exists():
            raise FileNotFoundError(f"File {supply_file} does not exist")

        self.__supply_file = supply_file
        if self.__transit is not None:
            self.__transit._set_supply_file(supply_file)

    def set_result_file(self, result_file: Path):
        """

        :param supply_file:
        :return:
        """

        if not os.path.isfile(result_file):
            raise FileNotFoundError(f"File {result_file} does not exist")

        self.__result_file = result_file
