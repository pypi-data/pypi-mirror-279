import sqlite3

import pandas as pd

from .data_record import DataRecord


class MicromobilityDock(DataRecord):
    def __init__(self, element_id, data_tables, geotool, conn=None):
        super(MicromobilityDock, self).__init__(element_id, "Micromobility_Docks", data_tables, pd.DataFrame(), conn)
        self.geotool = geotool
        if self.geo:
            self.box = self.geo.bounds

    def save(self, conn: sqlite3.Connection):
        super(MicromobilityDock, self).save(conn)
        self._data.refresh_cache("mobility_docks")

    def update_zone(self, commit=True):
        self.zone = self.geotool.get_zone(self.geo)

        if commit:
            self.save()

    def update_link(self, commit=True):
        self.link = self.geotool.get_link_for_point_by_mode(self.geo, ["AUTO"])[0]
        self.offset = self.geotool.links[self.link].project(self.geo)
        self.setback = self.geotool.links[self.link].distance(self.geo)
        self.dir = self.geotool.side_of_link_for_point(link=self.link, point=self.geo)

        if commit:
            self.save()
