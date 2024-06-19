from collections import OrderedDict
from os import PathLike

from polaris.utils.database.db_utils import read_and_close


def busy_nodes(number_connections: int, path_to_file: PathLike) -> OrderedDict:
    """Searches the network for links that have too many connections

    Args:
            *number_connections* (:obj:`int`): The maximum "normal" number of links connected to a node

    Returns:
            *occurences* (:obj:`OrderedDict`): Order dictionary with keys for links and values for number of connections

    ::

        from polaris.network.network import Network
        from polaris.network.checker.checks.busy_nodes import busy_nodes

        net = Network()
        net.open('path/to/my/network/file.sqlite')

        # Let's search for nodes with MORE THAN 6 links connected to it
        results = busy_nodes(number_connections=6)
        for link, connections in results.items():
            print(f'Link {link} has {connections} connections')

        net.close()
    """
    sql = f"""select node, counter from
        (select node_a node, tota+totb counter from (select node_a, count(*) tota from Link group by node_a) l
        inner join (select node_b, count(*) totb from Link group by node_b) r
        where l.node_a = r.node_b)
        where counter > {number_connections}
        order by counter DESC"""

    with read_and_close(path_to_file) as conn:
        occurrences = OrderedDict()
        for node, counter in conn.execute(sql).fetchall():
            occurrences[node] = counter
    return occurrences
