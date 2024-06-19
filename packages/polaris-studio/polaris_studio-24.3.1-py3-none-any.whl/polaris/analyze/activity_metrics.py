from copy import deepcopy
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd
from polaris.runs.scenario_compression import ScenarioCompression
from polaris.utils.database.db_utils import commit_and_close

fail_modes = ["NO_MOVE", "FAIL_ROUTE", "FAIL_REROUTE", "FAIL_MODE"]


class ActivityMetrics:
    """Loads all data required for the computation of metrics on activities.

    The behavior of time filtering consists of setting to instant zero
    whenever *from_time* is not provided and the end of simulation when
    *to_time* is not provided"""

    def __init__(self, supply_file: Path, demand_file: Path):
        """
        :param supply_file: Path to the supply file corresponding to the demand file we will compute metrics for
        :param demand_file: Path to the demand file we want to compute metrics for
        """

        self.period_definition = {
            "DAY": (0, 24),
            "NIGHT": (0, 5),
            "AMPEAK": (6, 8),
            "AMOFFPEAK": (9, 11),
            "PMOFFPEAK": (12, 15),
            "PMPEAK": (16, 18),
            "EVENING": (19, 24),
        }
        self.__demand_file = ScenarioCompression.maybe_extract(demand_file)
        self.__supply_file = supply_file
        self.__mode: Optional[str] = None
        self.__start = 0
        self.__end = 24
        self.__period = "DAY"
        self.__data = pd.DataFrame([])
        self.__loc_table = pd.DataFrame([])
        self.__zone_table = pd.DataFrame([])
        self.__all_modes: List[str] = []
        self.__all_types: List[str] = []
        self.__mode_share = False

    def get_trips(self, aggregation="zone") -> pd.DataFrame:
        """Queries all trips for the current set of filters and for the aggregation of choice

        :param aggregation: Filter to see either location or zone. Default is "zone"
        :return: Statistics DataFrame
        """

        df = self.data[(self.data.trip > 0) & (~self.data["mode"].isin(fail_modes))]

        df = df[(df.start_hour >= self.__start) & (df.start_hour <= self.__end)]

        if self.__mode is not None:
            if self.__mode_share:
                df = df.groupby([aggregation, "mode"]).count()[["trip"]]

                df.reset_index(inplace=True)
                df = pd.pivot_table(df, columns="mode", values="trip", index="zone", fill_value=0)
                df = df.assign(mode_share=df[self.__mode] / df.sum(axis=1))
                df.fillna(0, inplace=True)
                df = df[["mode_share"]]
                df.columns = ["trips"]  # type: ignore # Recommended Pandas behaviour that should not trigger typing
                return df
            else:
                df = df[df["mode"] == self.__mode]
        return df.groupby([aggregation]).count()[["trip"]].rename(columns={"trip": "trips"})

    def set_mode(self, mode: str, mode_share=False):
        """"""
        if mode in [None, "ALL", ""]:
            self.__mode = None
            return
        assert mode.upper() in [x.upper() for x in self.modes]
        self.__mode = mode.upper()
        self.__mode_share = mode_share

    def set_start_hour(self, start_hour: int):
        """"""
        assert 0 <= start_hour < 24
        self.__start = int(start_hour)

    def set_end_hour(self, end_hour: int):
        """The hour for the end (INCLUDED) of the period."""
        assert 1 <= end_hour < 24
        self.__end = int(end_hour)

    def set_time_period(self, time_period: str):
        """sets the time period we want to retrieve statistics about"""

        assert time_period.upper() in self.period_definition

        self.__period = time_period.upper()
        self.__start, self.__end = self.period_definition[self.__period]

    @property
    def modes(self):
        if not self.__all_modes:
            self.__all_modes = ["ALL"] + self.data["mode"].unique().tolist()
            self.__all_modes = [x for x in self.__all_modes if x not in fail_modes]
        return deepcopy(self.__all_modes)

    @property
    def types(self):
        if not self.__all_types:
            self.__all_types = ["ALL"] + self.data["type"].unique().tolist()
        return deepcopy(self.__all_types)

    @property
    def data(self) -> pd.DataFrame:
        if not self.__data.shape[0]:
            sql = """Select location_id as location, start_time, "mode", "type", "trip"  from Activity"""
            with commit_and_close(self.__demand_file) as conn:
                df = pd.read_sql(sql, conn)

            df = df.merge(self.locations, on="location")
            self.__data = df.assign(start_hour=np.floor(df.start_time / 3600)).dropna()

        return self.__data

    @property
    def locations(self) -> pd.DataFrame:
        if not self.__loc_table.shape[0]:
            with commit_and_close(self.__supply_file, spatial=True) as conn:
                self.__loc_table = pd.read_sql("Select location, zone from Location", conn)
        return self.__loc_table
