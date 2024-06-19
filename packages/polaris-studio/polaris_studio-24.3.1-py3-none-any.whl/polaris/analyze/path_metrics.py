from pathlib import Path
from typing import List

import pandas as pd
from polaris.runs.scenario_compression import ScenarioCompression
from polaris.utils.database.db_utils import commit_and_close


class PathMetrics:
    """Loads all data required for the computation of metrics on Paths."""

    def __init__(self, supply_file: Path, demand_file: Path):
        """
        :param supply_file: Path to the supply database corresponding to the demand file we will compute metrics for
        :param demand_file: Path to the result file we want to compute metrics for
        """
        self.__demand_file = ScenarioCompression.maybe_extract(demand_file)
        self.__supply_file = supply_file
        self.__start = 0
        self.__end = 24
        self.__data = pd.DataFrame([])
        self.__all_modes: List[str] = []
        self.__all_types: List[str] = []

    @property
    def data(self) -> pd.DataFrame:
        if not self.__data.shape[0]:
            sql = """SELECT
                     pl.object_id,
                     pl.value_link,
                     pl.value_travel_time,
                     pl.value_routed_travel_time,
                     pl.value_Number_of_Switches,
                     pl.value_Switch_Cause,
                     t.has_artificial_trip,
                     t.start tstart,
                     t.end tend,
                     t.mode tmode
                     FROM Path_links pl
                     INNER JOIN
                     Trip t
                     ON pl.object_id=t.path
                     WHERE (t.mode = 0 or t.mode = 9 or t.mode = 17 or t.mode = 18 or t.mode = 19 or t.mode = 20)
                     AND t.has_artificial_trip <> 1
                     AND t.end > t.start
                     AND t.routed_travel_time > 0
                     AND pl.value_travel_time>0;
                     """

            with commit_and_close(self.__demand_file) as conn:
                dt = pd.read_sql(sql, conn)

            dt.loc[dt.has_artificial_trip == 2, "absolute_gap"] = 2 * dt.value_routed_travel_time
            dt.loc[dt.has_artificial_trip.isin([0, 3, 4]), "absolute_gap"] = abs(
                dt.value_travel_time - dt.value_routed_travel_time
            )

            dt.loc[dt.absolute_gap < 0, "absolute_gap"] = 0
            self.__data = dt.assign(mstart=(dt.tstart / 60).astype(int), mend=(dt.tend / 60).astype(int))
        return self.__data
