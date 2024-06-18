import time
import logging
from types import FunctionType, ModuleType
from pathlib import Path

from .utils import EOvenScriptExecTime
from .config import Config

from .utils import load_module

INTERNAL_SCRIPTS_PATH = Path(__file__).parent / 'internal_scripts'


def is_valid_script(module: ModuleType) -> bool:
    return hasattr(module, 'SCRIPT_NAME') and hasattr(module, 'SCRIPT_EXEC_TIME') and hasattr(module, 'SCRIPT_ORDER') and hasattr(module, 'execute_script')


class ScriptsManager:
    class Script:
        def __init__(self, name: str, function: FunctionType, exec_time: EOvenScriptExecTime, order: int) -> None:
            self.name = name
            self.function = function
            self.exec_time = exec_time
            self.order = order

        def execute(self, config: Config, **kwargs) -> None:
            self.function(config, **kwargs)

    _instance = None

    def __init__(self, config: Config) -> None:
        self.config = config
        self.scripts = []

        self.__load_scripts(INTERNAL_SCRIPTS_PATH)
        self.__load_scripts(self.config.scripts_path)
        self.scripts.sort(key=lambda script: script.order)

    def __load_scripts(self, path: Path) -> None:
        if not path.exists():
            return
        loaded_scripts = 0

        logging.info(f'[Scripts] Loading scripts from {path}')
        for file in path.iterdir():
            if file.is_file() and file.suffix == '.py':
                module = load_module('oven_script', file)

                if is_valid_script(module):
                    if not self.config.enabled_scripts or module.SCRIPT_NAME in self.config.enabled_scripts:
                        logging.info(f'[Scripts] loaded script: {module.SCRIPT_NAME} with order: {module.SCRIPT_ORDER}')
                        loaded_scripts += 1
                        self.scripts.append(
                            ScriptsManager.Script(module.SCRIPT_NAME, module.execute_script, module.SCRIPT_EXEC_TIME,
                                                  module.SCRIPT_ORDER))
        logging.info(f'[Scripts] Loaded {loaded_scripts} scripts')

    def execute(self, exec_time: EOvenScriptExecTime) -> None:
        for script in self.scripts:
            if script.exec_time == exec_time:
                _start_time = time.time()
                script.execute(self.config, **self.config.scripts_config.get(script.name, {}))
                logging.info(f'[Scripts] script {script.name} took {time.time() - _start_time:.3f}s')
