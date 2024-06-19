from polaris.utils.database.db_utils import add_column_unless_exists


def migrate(conn):
    add_column_unless_exists(conn, "Vehicle", "Has_Residential_Charging", "INTEGER", "DEFAULT 0")
