import os
from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings

current_working_directory = Path.cwd()

filepath = os.path.join(os.path.dirname(__file__), "models")


class DBEnum(str, Enum):
    snowflake = "snowflake"
    duckdb = "duck"
    athena = "athena"
    databricks = "databricks"
    bigquery = "bigquery"


class Settings(BaseSettings):
    API_KEY: str = "some_secret"
    MODELS_PATH: str = filepath
    DB_TYPE: DBEnum = DBEnum.snowflake
    DB_USERNAME: str = ""
    DB_PASSWORD: str = ""
    DB_ACCOUNT: str = ""
