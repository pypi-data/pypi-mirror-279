from polaris.utils.database.standard_database import DatabaseType, StandardDatabase


def migrate(conn):
    StandardDatabase.for_type(DatabaseType.Demand).add_table(conn, "path_units", None, add_defaults=True)
