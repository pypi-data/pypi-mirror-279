from enum import Enum

from pathlib import Path
from typing import Optional
from types import ModuleType


from importlib import util as importlib_util


class EOvenScriptExecTime(Enum):
    START_BUILD = 0
    START_GATHER = 1
    FINISH_BUILD = 2
    FINISH_GATHER = 3


def load_module(name: str, path: Path) -> Optional[ModuleType]:
    spec = importlib_util.spec_from_file_location(name, path)
    filter_module = importlib_util.module_from_spec(spec)
    spec.loader.exec_module(filter_module)
    return filter_module
