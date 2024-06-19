def migrate(conn):
    from polaris.network.active.active_networks import ActiveNetworks

    ActiveNetworks.update_bearing(conn)
