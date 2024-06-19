from os.path import join, dirname, realpath
from sqlite3 import Connection

from polaris.network.starts_logging import logger


def recreate_network_triggers(conn: Connection, srid: int) -> None:
    delete_network_triggers(conn)
    create_network_triggers(conn, srid)


def create_network_triggers(conn: Connection, srid: int) -> None:
    logger.info("  Creating triggers")
    with open(join(dirname(realpath(__file__)), "../database/triggers/list_triggers.txt")) as f:
        trigger_list = [line.rstrip() for line in f.readlines()]

    for table in trigger_list:
        logger.debug(f"     creating triggers for {table}")
        qry_file = join(dirname(realpath(__file__)), "../database/triggers", f"{table}.sql")

        with open(qry_file, "r") as sql_file:
            query_list = sql_file.read()

        # Running one query/command at a time helps debugging in the case a particular command fails
        for cmd in query_list.split("--##"):
            if "SRID_PARAMETER" in cmd:
                cmd = cmd.replace("SRID_PARAMETER", f"{srid}")

            lines = [e.strip() for e in cmd.split("\n")]
            lines = [e for e in lines if not e.startswith("--") and e != ""]
            if not len(lines):
                continue
            try:
                conn.execute(cmd)
            except Exception as e:
                logger.error(f"Failed adding triggers table - > {e.args}")
                logger.error(f"Point of failure - > {cmd}")
                raise e
        conn.commit()


def delete_network_triggers(conn: Connection) -> None:
    logger.info("  Deleting triggers")
    with conn:
        with open(join(dirname(realpath(__file__)), "../database/triggers/list_triggers.txt")) as f:
            trigger_list = [line.rstrip() for line in f.readlines()]
        for table in trigger_list:
            qry_file = join(dirname(realpath(__file__)), "../database/triggers", f"{table}.sql")

            with open(qry_file, "r") as sql_file:
                query_list = sql_file.read()

            # Running one query/command at a time helps debugging in the case a particular command fails
            for cmd in query_list.split("--##"):
                for qry in cmd.split("\n"):
                    if qry[:2] == "--":
                        continue
                    if "create trigger if not exists " in qry:
                        qry = qry.replace("create trigger if not exists ", "")
                        qry = "DROP trigger if exists " + qry.split(" ")[0]
                        try:
                            conn.execute(qry)
                        except Exception as e:
                            logger.error(f"Failed removing triggers table - > {e.args}")
                            logger.error(f"Point of failure - > {qry}")
