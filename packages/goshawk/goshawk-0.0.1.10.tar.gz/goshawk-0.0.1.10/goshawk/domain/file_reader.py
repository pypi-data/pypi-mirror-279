import os
from typing import Any, Dict, List, Optional, Set

import yaml
from graphlib import CycleError, TopologicalSorter

from goshawk import app_settings
from goshawk.domain.exception import GoshawkException
from goshawk.logging import LOG


def dbpath_in_masks(foldername: str, masks: Optional[List[str]]) -> bool:
    LOG.debug(f"folder={foldername}")
    if not masks:
        return True
    LOG.debug(f"{masks=}")
    LOG.debug(f"{foldername=}")
    return any(mask.lower().startswith(foldername.lower()) for mask in masks)


def get_database_paths(masks: Optional[List[str]], models_path: Optional[str] = None) -> List[str]:
    models_path = models_path or app_settings.MODELS_PATH
    paths = [os.path.relpath(f.path) for f in os.scandir(models_path) if f.is_dir() and dbpath_in_masks(f.name, masks)]
    LOG.debug(f"{paths=}")
    if len(paths) > 1:
        raise GoshawkException("Only single database supported. Consider using the --mask option")
    return paths


def get_schema_paths(database_path: str) -> List[str]:
    return [f.path for f in os.scandir(database_path) if f.is_dir()]


def get_files(schema_path: str) -> List[str]:
    return [f.path for f in os.scandir(schema_path) if f.path.endswith(".sql")]


def get_schema_file(schema_path: str) -> List[str]:
    return [f.path for f in os.scandir(schema_path) if f.path.endswith("_schema.yml")]


def schema_in_mask(schema_path: str, mask: str) -> bool:
    schema_db = schema_path.split("/")[-2].upper()
    schema_name = schema_path.split("/")[-1].upper()
    mask_db = mask.split(".")[0].upper()
    mask_schema = mask.split(".")[1].upper()
    if mask_db != schema_db:
        LOG.debug(f"mask db {mask_db} not equal schema db {schema_db}")
        return False
    if mask_schema == "*":
        return True
    return mask_schema == schema_name


def schema_matches_mask(schema_path: str, masks: Optional[List[str]]) -> bool:
    if not masks:
        return True
    return any(schema_in_mask(schema_path, mask) for mask in masks)


def read_schema_file(filepath: str) -> Any:
    with open(filepath) as stream:
        try:
            contents = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return contents


def read_files(masks: Optional[List[str]] = None, path: str | None = None) -> List[Dict]:
    LOG.debug(f"reading files masks={masks} path={path}")
    retval = []
    for database_folder in get_database_paths(masks, path):
        for schema_folder in get_schema_paths(database_folder):
            if schema_matches_mask(schema_folder, masks):
                schema_file = get_schema_file(schema_folder)
                meta_data = read_schema_file(schema_file[0]) if schema_file else {}
                for sqlfile in get_files(schema_folder):
                    model = {
                        "database": database_folder,
                        "schema": schema_folder,
                        "name": sqlfile,
                        "filepath": sqlfile,
                        "schema_meta_data": meta_data,
                    }
                    retval.append(model)
    models = retval
    return models


def validate_schema_dag(schema_dag: Dict[str, Set[str]]) -> bool:
    ts: TopologicalSorter = TopologicalSorter(schema_dag)
    try:
        ts.prepare()
    except CycleError:
        return False
    return True
