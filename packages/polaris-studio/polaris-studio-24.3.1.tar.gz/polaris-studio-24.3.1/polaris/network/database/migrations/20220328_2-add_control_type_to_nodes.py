from polaris.utils.database.db_utils import add_column_unless_exists


def migrate(conn):
    add_column_unless_exists(conn, "NODE", "control_type", "TEXT", "DEFAULT ''")
