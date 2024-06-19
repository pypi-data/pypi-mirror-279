import pandas as pd


class BasicPTElement:
    def from_row(self, data: pd.Series):
        for key, value in data.items():
            if key not in self.__dict__.keys():
                raise KeyError(f"{key} Field does not exist")
            self.__dict__[key] = value  # type: ignore
        return self
