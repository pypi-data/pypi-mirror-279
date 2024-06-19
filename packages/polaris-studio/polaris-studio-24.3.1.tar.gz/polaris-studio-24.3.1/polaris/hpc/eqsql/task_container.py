import logging
import os
from typing import Any, NamedTuple

from polaris.hpc.eqsql.eq import insert_task_log, worker_id
from polaris.hpc.eqsql.task import Task
from sqlalchemy import Engine, create_engine


class TaskContainer(NamedTuple):
    """
    This class exists to collect together the data for a task so that it can be passed around as part of the
    config.user_data field.
    """

    engine: Engine
    payload: Any
    task: Task

    @classmethod
    def from_env(cls, payload=None):
        if "EQSQL_DB_CONN" in os.environ:
            engine = create_engine(os.environ["EQSQL_DB_CONN"], isolation_level="AUTOCOMMIT", pool_pre_ping=True)
            task = Task.from_id(engine, int(os.environ["EQSQL_TASK_ID"]))
            return cls(engine=engine, payload=payload, task=task)
        return cls(engine=None, payload=payload, task=None)

    def log(self, message):
        if self.engine is not None:
            self.log_to_engine(message)
        else:
            logging.info(message)

    def log_to_engine(self, message):
        try:
            with self.engine.connect() as conn:
                insert_task_log(conn, self.task.task_id, message, worker_id())
        except Exception:
            logging.error("Failed sending back log message to DB!!")
            logging.error(message)
