import numpy as np
from polaris.runs.results.result_version import get_version_from_handle
from tables import open_file


class H5_Results(object):
    def __init__(self, filename):
        self.filename = filename
        with open_file(self.filename, mode="r") as h5file:
            self.version = get_version_from_handle(h5file)
            self.num_timesteps = h5file.root.link_moe._v_attrs.num_timesteps

        self.num_links = self.get_vector("link_moe", "link_uids").shape[0]
        self.num_turns = self.get_vector("turn_moe", "turn_uids").shape[0]

    def get_vector(self, group, value):
        with open_file(self.filename, mode="r") as h5file:
            return np.array(h5file.root._f_get_child(group)._f_get_child(value)).flatten()

    def get_array(self, group, table):
        with open_file(self.filename, mode="r") as h5file:
            return np.array(h5file.root._f_get_child(group)._f_get_child(table))

    def get_array_v0(self, f, group, table):
        tables = {
            "link_moe": [
                "link_travel_time",
                "link_travel_time_standard_deviation",
                "link_queue_length",
                "link_travel_delay",
                "link_travel_delay_standard_deviation",
                "link_speed",
                "link_density",
                "link_in_flow_rate",
                "link_out_flow_rate",
                "link_in_volume",
                "link_out_volume",
                "link_speed_ratio",
                "link_in_flow_ratio",
                "link_out_flow_ratio",
                "link_density_ratio",
                "link_travel_time_ratio",
                "num_vehicles_in_link",
                "volume_cum_BPLATE",
                "volume_cum_LDT",
                "volume_cum_MDT",
                "volume_cum_HDT",
                "entry_queue_length",
            ],
            "turn_moe": [
                "turn_penalty",
                "turn_penalty_sd",
                "inbound_turn_travel_time",
                "outbound_turn_travel_time",
                "turn_flow_rate",
                "turn_flow_rate_cv",
                "turn_penalty_cv",
                "total_delay_interval",
                "total_delay_interval_cv",
            ],
        }
        return f[group][:, :, tables[group].index(table)].T
