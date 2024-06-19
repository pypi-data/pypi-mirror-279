from polaris.utils.database.db_utils import add_column_unless_exists


def migrate(conn):
    add_column_unless_exists(conn, "TNC_Request", "distance", "REAL", "DEFAULT 0.0")
    add_column_unless_exists(conn, "TNC_Trip", "toll", "REAL", "DEFAULT 0.0")
