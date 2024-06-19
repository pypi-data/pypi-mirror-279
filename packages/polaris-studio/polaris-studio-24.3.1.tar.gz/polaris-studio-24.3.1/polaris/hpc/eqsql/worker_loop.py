#!/usr/bin/env python3
import logging
import os
import signal
import sys
import traceback
from pathlib import Path
from socket import gethostname

from polaris.hpc.eqsql.eq import (
    EQ_TIMEOUT,
    get_next_task,
    update_worker,
    worker_id,
)
from polaris.hpc.eqsql.eq_db import DEAD, IDLE
from polaris.hpc.eqsql.task_runner import try_run_task_in_bg
from polaris.utils.db_config import DbConfig

POLARIS_DIR = Path(__file__).resolve().absolute().parent.parent.parent.parent


def main():
    setup_path()
    engine = setup_db_engine()
    loop(engine)


def setup_path():
    if str(POLARIS_DIR) not in sys.path:
        sys.path.append(str(POLARIS_DIR))

    # also set the path via env variable for any child processes we kick off
    if "PYTHONPATH" in os.environ:
        os.environ["PYTHONPATH"] = os.environ["PYTHONPATH"] + ":" + str(POLARIS_DIR)
    else:
        os.environ["PYTHONPATH"] = str(POLARIS_DIR)
    os.environ["WORKER_ID"] = os.environ.get("WORKER_ID", gethostname())


def setup_db_engine():
    db_config = DbConfig.from_json_file(sys.argv[1]) if len(sys.argv) > 1 else DbConfig()

    # Store the connection string so that spawned jobs can establish their own connection for status updates
    os.environ["EQSQL_DB_CONN"] = db_config.conn_string()

    # Create the engine and test it can connect
    engine = db_config.create_engine()
    with engine.connect() as conn:
        conn.commit()
    return engine


def loop(engine):
    heartbeat_interval = 120.0
    idle_shutdown = int(os.environ.get("EQSQL_idle_shutdown", 0))
    idle_timer = 0.0 if idle_shutdown > 0 else None
    logging.info(f"{heartbeat_interval=}")
    logging.info(f"{idle_shutdown=}")
    logging.info(f"{idle_timer=}")

    while True:
        try:
            logging.info("trying to get task...")
            with engine.connect() as conn:
                # send heartbeat
                update_worker(conn, worker_id(), None, IDLE, "Waiting for work")

                # try to get a task
                result = get_next_task(conn, eq_type=1, delay=0.25, timeout=heartbeat_interval, worker_id=worker_id())

            if result.succeeded:
                try_run_task_in_bg(engine, result.value)
            elif result.reason != EQ_TIMEOUT:
                logging.error("Something went wrong, restarting!")
                logging.error(result.reason)
                exit(1)
            elif idle_timer is not None:
                idle_timer += heartbeat_interval
                if idle_timer >= idle_shutdown:
                    logging.info(f"Node idle time ({idle_timer}) exceeded idle_shutdown threshold ({idle_shutdown})")
                    Path(os.environ["WORKER_LOOP_RUN_FILE"]).unlink()
                    with engine.connect() as conn:
                        update_worker(conn, worker_id(), None, DEAD, "Shutdown by idle_shutdown")
                    exit(0)

        except Exception:
            logging.info("An error occurred while handling a task.")
            logging.info(traceback.format_exc())
            logging.info("Exiting so that outer-loop can restart me")
            exit(1)


def signal_handler(signum, frame):
    logging.info("Gracefully exiting loop")
    logging.info(frame)
    exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
