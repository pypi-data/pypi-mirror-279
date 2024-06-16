from snowflake.connector import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor

from goshawk.domain.model import SQLModel
from goshawk.logging import LOG

from ..settings import Settings


class base_adapter:
    def __init__(self) -> None:
        self.connection = None
        self.settings = Settings()

    def connect(self) -> None:
        pass

    def execute_sql(self, sql: str) -> SnowflakeCursor:
        LOG.info(f"executing {sql}")
        return SnowflakeCursor(SnowflakeConnection())

    def create_schema(self, db: str, schema: str) -> None:
        self.execute_sql(f"CREATE SCHEMA {schema}")

    def create_database(self, db: str) -> None:
        pass

    def deploy_model(self, target_schema: str, model: SQLModel) -> None:
        pass

    def get_models_in_db(self, dbname: str) -> SnowflakeCursor:
        return self.execute_sql("dummy")

    def clone_db(self, source_db: str, target_db: str) -> None:
        pass
