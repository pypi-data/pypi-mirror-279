from copy import deepcopy
from os import PathLike
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from polaris.runs.scenario_compression import ScenarioCompression
from polaris.utils.database.db_utils import read_and_close


class TripMetrics:
    """Loads all data required for the computation of metrics on Trips.

    The behavior of time filtering consists of setting to instant zero
    whenever *from_time* is not provided and the end of simulation when
    *to_time* is not provided"""

    def __init__(self, supply_file: PathLike, demand_file: PathLike):
        """
        :param supply_file: Path to the supply file corresponding to the demand file we will compute metrics for
        :param demand_file: Path to the demand file we want to compute metrics for
        """
        self.__demand_file = Path(demand_file)
        self.__supply_file = Path(supply_file)
        self.__start = 0
        self.__end = 24
        self.__data = pd.DataFrame([])
        self.__all_modes: List[str] = []
        self.__all_types: List[str] = []

    @property
    def modes(self):
        if not self.__all_modes:
            self.__all_modes = ["ALL"] + self.data["tmode"].unique().tolist()
        return deepcopy(self.__all_modes)

    @property
    def artificial_trips(self):
        if not self.__all_types:
            self.__all_types = ["ALL"] + self.data["has_artificial_trip"].unique().tolist()
        return deepcopy(self.__all_types)

    @property
    def data(self) -> pd.DataFrame:
        if not self.__data.shape[0]:
            sql = """Select trip_id,
                     path,
                     mode as tmode,
                     start tstart,
                     end tend,
                     origin,
                     destination,
                     has_artificial_trip,
                     routed_travel_time,
                     travel_distance,
                     0 absolute_gap
                     from Trip
                     WHERE (mode = 0 or mode = 9 or mode = 17 or mode = 18 or mode = 19 or mode = 20)
                     AND has_artificial_trip <> 1
                     AND end > start
                     AND routed_travel_time > 0;
                     """

            ScenarioCompression.maybe_extract(self.__demand_file)
            with read_and_close(self.__demand_file) as conn:
                trips = pd.read_sql(sql, conn)
            trips["absolute_gap"] = trips.absolute_gap.astype(np.float64)
            trips.loc[trips.has_artificial_trip == 0, "absolute_gap"] = abs(
                trips.tend - trips.tstart - trips.routed_travel_time
            )
            trips.loc[trips.has_artificial_trip == 2, "absolute_gap"] = 2 * trips.routed_travel_time
            trips.loc[trips.has_artificial_trip.isin([3, 4]), "absolute_gap"] = (
                trips.tend - trips.tstart - trips.routed_travel_time
            )

            trips.loc[trips.absolute_gap < 0, "absolute_gap"] = 0
            trips = trips.assign(hstart=(trips.tstart / 3600).astype(int), hend=(trips.tend / 3600).astype(int))
            self.__data = trips.assign(mstart=(trips.tstart / 60).astype(int), mend=(trips.tend / 60).astype(int))
        return self.__data
