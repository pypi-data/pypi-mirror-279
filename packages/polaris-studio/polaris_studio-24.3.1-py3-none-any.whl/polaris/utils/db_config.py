from polaris.utils.config_utils import from_json_file
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine


class DbConfig(BaseModel):
    # The following is here to avoid problems in the Cython compiled version of polaris.
    # When compiled, methods (including methods of this class) are no longer "function"s they become "cyfunctions".
    # We use type(from_json_file) to get that type at runtime so that pydantic doesn't try to check the methods are
    # annotated.
    model_config = ConfigDict(ignored_types=(type(from_json_file),))

    host: str = "vms-pol-pg.taps.anl.gov"
    port: int = 5432
    db_name: str = "eqsql_db"
    user: str = "eqsql_user"
    password: str = "polaris"

    def conn_string(self):
        # returns: postgresql+psycopg://eqsql_user@vms-pol-pg.taps.anl.gov:5432/eqsql_db
        if self.password is not None:
            return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        return f"postgresql+psycopg://{self.user}@{self.host}:{self.port}/{self.db_name}"

    @classmethod
    def from_json_file(cls, filename):
        return from_json_file(cls, filename)

    def create_engine(self):
        return create_engine(self.conn_string(), isolation_level="AUTOCOMMIT", pool_pre_ping=True)
