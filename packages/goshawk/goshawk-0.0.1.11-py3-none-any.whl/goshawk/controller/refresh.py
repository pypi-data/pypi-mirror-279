from graphlib import TopologicalSorter

import goshawk.domain as domain
from goshawk.logging import LOG

from .. import app_settings
from ..utils import get_adapter

LOG.debug("deployer loading")

Adapter = get_adapter(app_settings.DB_TYPE.value)


def schema_in_mask(schema_name: str, mask: str) -> bool:
    schema_db = schema_name.split(".")[0].upper()
    mask_db = mask.split(".")[0].upper()
    mask_schema = mask.split(".")[1].upper()
    if mask_db != schema_db:
        LOG.debug(f"mask db {mask_db} not equal schema db {schema_db}")
        return False
    if mask_schema == "*":
        return True
    return mask.upper() == schema_name.upper()


def schema_matches_any_mask(schema_name: str, masks: list[str]) -> bool:
    return not masks or any(schema_in_mask(schema_name, m) for m in masks)


def convert_schema(target_db: str, qualified_schema: str) -> str:
    if qualified_schema.startswith(target_db):
        return qualified_schema
    else:
        return target_db + "." + qualified_schema.split(".")[1]


def refresh_models() -> None:
    LOG.debug(domain.cli_params)
    if domain.cli_params.get("dry_run"):
        return
    LOG.info("Refreshing data")

    dag = domain.models.schema_dag
    mask = domain.cli_params.get("mask", [])

    ts = TopologicalSorter(dag)
    suffix = "refreshtmp"
    if domain.cli_params.get("db_env"):
        target_db = domain.models.db + "_" + domain.cli_params.get("db_env", "")
    else:
        target_db = domain.models.db

    LOG.debug(f"Refreshing data using masks {mask} in database {target_db}")
    # TODO: make sure db exists

    # Adapter.create_database(domain.models.db)
    for schema in ts.static_order():
        if schema_matches_any_mask(schema, mask):
            if domain.cli_params.get("db_env"):
                work_schema = schema
            else:
                work_schema = f"{schema}_{suffix}"
                Adapter.clone_schema(schema, work_schema)
            LOG.debug(f"Refreshing schema {schema} in {work_schema}")
            refresh_schema(target_db, schema, work_schema)
            if not domain.cli_params.get("db_env"):
                Adapter.swap_schema(work_schema, schema)


def refresh_schema(target_db: str, child_schema: str, work_schema: str) -> None:
    LOG.debug(f"in refresh_schema target_db={target_db}, child_schema={child_schema}, work_schema={work_schema}")
    target_schema = convert_schema(target_db, work_schema)
    LOG.debug(f"target_schema = {target_schema}")
    model_dag = domain.models.filtered_dag(child_schema)
    ts = TopologicalSorter(model_dag)
    for fqn in ts.static_order():
        if fqn.startswith(child_schema):
            if domain.models.sql_models.get(fqn):
                thismodel = domain.models.sql_models.get(fqn)
                if thismodel and thismodel._materialization == "table":
                    LOG.debug(f"Refreshing model {fqn} in schema {work_schema}")
                    Adapter.refresh_model(target_schema, domain.models.sql_models[fqn]._name)
                else:
                    LOG.debug(f"Model {fqn} is a view")
                # Adapter.refresh_model(target_schema, domain.models.sql_models[fqn].)
            else:
                LOG.debug(f"Model {fqn} does not exist in collection")
        else:
            LOG.debug(f"Model {fqn} is in another schema")
