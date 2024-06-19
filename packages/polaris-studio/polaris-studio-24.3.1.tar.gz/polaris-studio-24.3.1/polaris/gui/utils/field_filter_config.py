from dataclasses import dataclass

import numpy as np
import pandas as pd
from polaris.utils.database.db_utils import ColumnDef


@dataclass
class FieldFilterConfig:
    field_type: ColumnDef
    values: list
    table: str
    min_val = 0.0
    max_val = 1e300
    populated = False

    def populate(self, df: pd.DataFrame):
        if self.populated:
            return

        fld = self.field_type.name
        if self.field_type.type in ["TEXT", "INTEGER"]:
            unique = df[fld].unique()
            if len(unique) < 50 or self.field_type.type == "TEXT":
                self.values = sorted(unique)
        if self.field_type.type != ["TEXT"] and len(self.values) == 0:
            self.min_val = np.nanmin(df[fld])
            self.max_val = np.nanmax(df[fld])
        self.populated = True
