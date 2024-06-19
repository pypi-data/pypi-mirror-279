import sqlite3

from polaris.utils.database.db_utils import read_about_model_value


def driving_side(conn: sqlite3.Connection):
    side = read_about_model_value(conn, "hand_of_driving", cast=str, default="RIGHT")
    return -1 if side.upper() == "LEFT" else 1
