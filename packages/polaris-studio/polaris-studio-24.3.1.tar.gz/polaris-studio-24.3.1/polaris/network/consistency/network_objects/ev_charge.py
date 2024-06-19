import pandas as pd

from .data_record import DataRecord


class EVChargeStation(DataRecord):
    def __init__(self, station_id: int, data_tables, conn=None):
        self.Latitude: float
        self.Longitude: float
        self.location: int
        self.zone: int
        self.public_flag: int
        super().__init__(station_id, "EV_Charging_Stations", data_tables, pd.DataFrame([]), conn)
