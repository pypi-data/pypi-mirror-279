from __future__ import annotations  # Should be able to remove in py 3.10

from enum import Enum
from typing import Any

from sqlglot import ParseError, exp, parse_one

from goshawk.logging import LOG

from .file_reader import read_files

# from .. import settings

LOG.debug("model initialization")
SQL_DIALECT = "snowflake"


class SourceTable:
    def __init__(self, fqn: str, table_exp: exp.Table):
        parts = fqn.split(".")
        db = parts[0]
        schema = db + "." + parts[1]

        if len(table_exp.parts) == 3:
            assert isinstance(table_exp.parts[0], exp.Identifier)  # this pleases mypy
            assert isinstance(table_exp.parts[1], exp.Identifier)
            self.table_catalog = (
                table_exp.parts[0].name if table_exp.parts[0].quoted else table_exp.parts[0].name.upper()
            )
            self.table_schema = (
                self.table_catalog + "." + table_exp.parts[1].name
                if table_exp.parts[1].quoted
                else self.table_catalog + "." + table_exp.parts[1].name.upper()
            )
        if len(table_exp.parts) == 2:
            assert isinstance(table_exp.parts[0], exp.Identifier)
            self.table_schema = (
                db + "." + table_exp.parts[0].name
                if table_exp.parts[0].quoted
                else db + "." + table_exp.parts[0].name.upper()
            )
            self.table_catalog = db
        if len(table_exp.parts) == 1:
            self.table_schema = schema
            self.table_catalog = db
        self.table_name = table_exp.name if getattr(table_exp.this, "quoted", None) else table_exp.name.upper()
        self.fqn = f"{self.table_schema}.{self.table_name}"


class ModelTypes(str, Enum):
    view = "view"
    table = "table"


class SQL_Parse(Exception):
    pass


def fqn_schema(fqn: str) -> str:
    if len(fqn.split(".")) != 3 and 1 == 2:
        raise SQL_Parse()
    return f"{fqn.split('.')[0]}.{fqn.split('.')[1]}"


class SQLModel:
    def __init__(
        self, database: str, schema: str, name: str, filepath: str, schema_meta_data: dict[str, Any] | None = None
    ):
        if not schema_meta_data:
            schema_meta_data = {}
        self._filepath = filepath
        self._database = filepath.split("/")[-3].upper()
        self._schema = self._database + "." + filepath.split("/")[-2].upper()
        self._name = filepath.split("/")[-1].upper().removesuffix(".SQL")
        self._schema_meta_data = schema_meta_data
        self._meta_data = schema_meta_data.get(self._name)
        if self._meta_data:
            self._materialization = self._meta_data.get("materialization", "view")
        else:
            self._materialization = "view"
        self.fqn = f"{self._schema}.{self._name}"
        with open(filepath) as f:
            self._raw_sql = f.read()
        try:
            self._parsed_sql = parse_one(self._raw_sql, dialect=SQL_DIALECT)
        except ParseError as e:
            raise SQL_Parse(f"Error parsing {filepath}") from e
        self._ctes = [ex.alias_or_name.upper() for ex in self._parsed_sql.find_all(exp.CTE)]

        self._table_references = [
            t
            for t in self._parsed_sql.find_all(exp.Table)
            if (t.name.upper() not in self._ctes) and (t.this.key != "anonymous")
        ]
        self.parent_tables = {}
        for t in self._table_references:
            source_table = SourceTable(self.fqn, t)
            self.parent_tables[source_table.fqn] = source_table

        self.schemas = {f"{fqn_schema(t)}" for t in self.parent_tables if fqn_schema(t) != self._schema}


class ModelCollection:
    def __init__(self) -> None:
        self._sql_models: dict[str, SQLModel] = {}
        self._schema_dag: dict[str, set[str]] = {}
        self._models_dag: dict[str, set[str]] = {}
        self.cli_params: dict[str, Any] = {}

    def _reset(self) -> None:
        pass

    def filtered_dag(self, schema: str) -> dict[str, set[str]]:
        return {k: v for k, v in self.models_dag.items() if k.startswith(schema)}

    @property
    def db(self) -> str:
        return next(iter(self.sql_models.values()))._database

    def clear_state(self) -> None:
        LOG.debug("Clearing state")
        self._sql_models.clear()
        self._schema_dag.clear()
        self._models_dag.clear()

    @property
    def sql_models(self) -> dict[str, SQLModel]:
        if not self._sql_models:
            self.reload_models()
        return self._sql_models

    def reload_models(self, path: str | None = None, mask: list[str] | None = None) -> None:
        LOG.debug(f"Reloading models path= {path}")
        self.clear_state()
        if not mask:
            mask = self.cli_params.get("mask")
        LOG.debug(f"Reloading models path= {path}, mask={mask}")
        sql_files = read_files(mask, path)
        for file in sql_files:
            model = SQLModel(**file)
            self._sql_models[model.fqn] = model
            LOG.debug(f"adding {model.fqn}")
        return

    @property
    def schema_dag(self) -> dict[str, set[str]]:
        if not self._schema_dag:
            self._schema_dag = self.build_schema_dag(self.sql_models)
        return self._schema_dag

    @property
    def models_dag(self) -> dict[str, set[str]]:
        if not self._models_dag:
            self._models_dag = self.build_models_dag(self.sql_models)
        return self._models_dag

    @classmethod
    def build_schema_dag(self, models: dict[str, SQLModel]) -> dict[str, set[str]]:
        schemas: dict[str, set[str]] = {}
        for _, m in models.items():
            if m._schema not in schemas:
                schemas[m._schema] = set()

            for parent_schema in m.schemas:
                if parent_schema != m._schema:
                    schemas[m._schema].add(parent_schema)

        return schemas

    @classmethod
    def build_models_dag(self, models: dict[str, SQLModel]) -> dict[str, set[str]]:
        child_models: dict[str, set[str]] = {}
        for fqn, m in models.items():
            child_models[fqn] = set()
            for parent_model in m.parent_tables:
                child_models[fqn].add(parent_model)
        return child_models
