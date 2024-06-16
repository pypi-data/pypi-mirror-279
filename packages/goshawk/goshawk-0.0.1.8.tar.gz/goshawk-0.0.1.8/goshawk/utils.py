import importlib

from .adapters.base_adapter import base_adapter
from .logging import LOG


def get_adapter(dbtype: str) -> base_adapter:
    module = importlib.import_module(f"goshawk.adapters.{dbtype}_adapter")
    LOG.debug(f"Adapter = {module}")
    class_ = getattr(module, dbtype)
    ret = class_()
    assert isinstance(ret, base_adapter)
    return ret
