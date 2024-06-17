from typing import Any

from goshawk.domain.model import ModelCollection
from goshawk.logging import LOG

LOG.debug("In domain.init")
models = ModelCollection()


cli_params: dict[str, Any] = {}
models.cli_params = cli_params
# this is where I want to store "global state"
_all__ = ["models", "cli_params"]
