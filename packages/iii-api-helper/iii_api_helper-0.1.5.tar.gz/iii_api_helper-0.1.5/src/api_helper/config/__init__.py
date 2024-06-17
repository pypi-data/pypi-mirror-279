from .configure import get
from .configure import load_config
from .formatter import ConsoleFormatter
from .formatter import TimedAccessFormatter
from .logger import LoggerBuilder


def is_debug() -> bool:
    return get("DEBUG", False, convert=True)


def is_reload() -> bool:
    return get("RELOAD", False, convert=True)
