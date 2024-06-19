from os import PathLike

import numpy as np
import pandas as pd

INFINITE_TRANSIT = 1e6


class SkimBase:
    def __init__(self):
        self.version = "omx"
        self._inf = np.inf
        self.zone_id_to_index_map = {}
        self.zone_index_to_id_map = {}
        self.index = pd.DataFrame([])
        self.intervals = []

    @classmethod
    def from_file(self, path_to_file: PathLike):
        mat = self()
        mat.open(path_to_file)
        return mat

    @property
    def num_zones(self) -> int:
        return self.index.shape[0]

    def open(self, path_to_file: PathLike):
        """Method overloaded by each skim class type"""
        pass

    def __setattr__(self, key, value):
        self.__dict__[key] = value

        if key != "index":
            return
        self.zone_id_to_index_map.clear()
        self.zone_index_to_id_map.clear()

        if value.shape[0]:
            self.zone_id_to_index_map = dict(zip(value.zones, value.index))
            self.zone_index_to_id_map = dict(zip(value.index, value.zones))
