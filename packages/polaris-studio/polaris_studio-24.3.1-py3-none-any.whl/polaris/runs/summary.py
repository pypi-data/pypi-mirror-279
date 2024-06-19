import logging
import os
from glob import glob
from os.path import join
from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError


def load_summary(summary_path, raise_on_error=True, drop_last_minute=True):
    try:
        df = pd.read_csv(summary_path, index_col=False, on_bad_lines="warn")
        if drop_last_minute:
            df = df[df.simulated_time < (86400 - 60)]
        if df["pax_in_network"].isna().any():
            logging.warning(f"Error while reading file ({summary_path}), last 10 lines are: ")
            with open(summary_path, "r") as f:
                for line in f.readlines()[-10:]:
                    logging.info(line.strip())
            if raise_on_error:
                raise ValueError("BLAH")
            else:
                # We are using pax_in_network column to look for mis-formed csv files
                # if we are ignoring errors - just drop any rows where this column is NA
                return df[~df["pax_in_network"].isna()]
        return df
    except EmptyDataError:
        # After certain conditions (i.e. warm start) no summary file will be generated
        return None


def parse_row(row):
    print(f"row = {row}")
    for col, parser in summary_types.items():
        row[col] = parser(row[col])
    return row


def time_parser(val):
    h, m, s = map(int, val.split(":"))
    return h * 3600 + 60 * m + s


summary_types = {"time": time_parser, "departed": int}


def find_summary_files(base_dir, db_name):
    return sorted(glob(join(base_dir, f"{db_name}*", "summary*.csv")), key=os.path.getmtime)


def aggregate_summaries(base_dir, db_name, save=True):
    summary_list = find_summary_files(base_dir, db_name)

    if len(summary_list) == 0:
        print("No summary files found in directory: " + base_dir)
        return pd.DataFrame()

    df = aggregate_summaries_from_list(summary_list)
    if save:
        df.to_csv(base_dir / "aggregate_summary.csv")

    return df


def aggregate_summaries_from_list(summary_list):
    df = pd.DataFrame()
    for i, summary in enumerate(summary_list):
        try:
            s = pd.read_csv(summary, index_col=False)
        except pd.errors.EmptyDataError:
            continue

        # If this is the first valid summary file - use it to get the index column (datetime)
        if df.shape[0] == 0:
            df["time"] = s["time"]
        name = Path(summary).parent.name
        df[name + "_in_network"] = s["in_network"]
        df[name + "_pax_in_network"] = s["pax_in_network"]

    return df
