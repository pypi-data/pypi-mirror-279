from polaris.utils.database.db_utils import add_column_unless_exists


def migrate(conn):
    add_column_unless_exists(conn, "Trip", "request", "INT", "DEFAULT 0")
    add_column_unless_exists(conn, "TNC_Trip", "request", "INT", "DEFAULT 0")
