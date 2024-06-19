from polaris.network.create.triggers import recreate_network_triggers
from polaris.network.database_connection import get_srid


def migrate(conn):
    recreate_network_triggers(conn, get_srid(conn=conn))
