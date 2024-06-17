from typing import Optional

import snowflake.connector as sfconnector
from snowflake.connector import DictCursor, SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor

from goshawk.adapters.base_adapter import base_adapter
from goshawk.domain.model import SQLModel
from goshawk.logging import LOG


class snowflake(base_adapter):
    def __init__(self) -> None:
        super().__init__()
        self.dialect = "snowflake"
        self.con: Optional[SnowflakeConnection] = None

    def connect(self) -> None:
        if not self.con:
            self.con = sfconnector.connect(
                user=self.settings.DB_USERNAME,
                password=self.settings.DB_PASSWORD,
                account=self.settings.DB_ACCOUNT,
                warehouse="compute_wh",
                session_parameters={
                    "QUERY_TAG": "goshawk",
                },
            )
            self.con.execute_string("use warehouse compute_wh")

    def execute_sql(self, sql: str) -> SnowflakeCursor:
        LOG.debug(f"Executing\n{sql}")
        self.connect()
        assert isinstance(self.con, SnowflakeConnection)
        c = self.con.cursor(DictCursor)
        try:
            c.execute(sql)
        except Exception as e:
            print(sql)
            print(e)
            raise ValueError(e) from e
        return c

    def deploy_model(self, target_schema: str, model: SQLModel) -> None:
        LOG.info(f"Creating model {model.fqn} in snowflake")
        self.execute_sql(f"USE {target_schema}")
        if model._materialization == "view":
            self.execute_sql(f"CREATE VIEW {model._name} as {model._raw_sql}")
        else:
            self.execute_sql(f"CREATE VIEW {model._name}_source as {model._raw_sql}")
            self.execute_sql(f"CREATE TABLE {model._name} as select * from {model._name}_source")

    def create_schema(self, dbname: str, schema: str) -> None:
        self.execute_sql(f"create or replace schema {schema}")

    def create_database(self, dbname: str) -> None:
        # assert isinstance(self.con, DictCursor)
        self.execute_sql(f'create or replace database "{dbname.upper()}"')
        LOG.debug(f"Created database {dbname} in Snowflake")

    def get_models_in_db(self, dbname: str) -> SnowflakeCursor:
        sql = f"select table_schema,table_name,table_type,created,row_count from {dbname}.information_schema.tables where table_schema<>'INFORMATION_SCHEMA' order by created"
        tables = self.execute_sql(sql)
        return tables

    def clone_db(self, source_db: str, target_db: str) -> None:
        sql = f"CREATE OR REPLACE DATABASE {target_db} CLONE {source_db}"
        self.execute_sql(sql)

    def clone_schema(self, source_schema: str, target_schema: str) -> None:
        sql = f"CREATE OR REPLACE SCHEMA {target_schema} CLONE {source_schema}"
        self.execute_sql(sql)

    def swap_schema(self, source_schema: str, target_schema: str) -> None:
        sql = f"ALTER SCHEMA {target_schema} SWAP WITH {source_schema}"
        self.execute_sql(sql)

    def refresh_model(self, target_schema: str, model_name: str) -> None:
        target_obj = f"{target_schema}.{model_name}"
        source_view = f"{target_schema}.{model_name}_source"
        sql = f"INSERT OVERWRITE INTO {target_obj} SELECT * FROM {source_view}"
        self.execute_sql(sql)
