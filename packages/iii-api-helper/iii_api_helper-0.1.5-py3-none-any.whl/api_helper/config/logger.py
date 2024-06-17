import logging.config
from logging import Logger
from logging import getLogger
from pathlib import Path
from typing import Any

from typing_extensions import Self

from .. import config
from .formatter import ConsoleFormatter
from .formatter import TimedAccessFormatter

logger: Logger = getLogger(__name__)

FORMATS: dict[str, str] = {
    "default": "[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
    "access": (
        "[%(levelname)s] %(asctime)s %(client_addr)s - %(run_time)s "
        '"%(request_line)s" %(status_code)s %(response_length)s'
    ),
}
FORMATTER: dict[str, type[logging.Formatter]] = {
    "console": ConsoleFormatter,
    "access": TimedAccessFormatter,
}
FORMATTERS: dict[str, Any] = {
    "console": {
        "()": FORMATTER["console"],
        "fmt": FORMATS["default"],
        "use_colors": True,
    },
    "file": {
        "()": FORMATTER["console"],
        "fmt": FORMATS["default"],
    },
    "access": {
        "()": FORMATTER["access"],
        "fmt": FORMATS["access"],
        "use_colors": True,
    },
    "access_file": {
        "()": FORMATTER["access"],
        "fmt": FORMATS["access"],
        "use_colors": False,
    },
}
HANDLER: dict[str, str] = {
    "stream": "logging.StreamHandler",
    "file": "logging.handlers.TimedRotatingFileHandler",
}


class LoggerBuilder:
    __slots__ = (
        "base_folder",
        "files",
        "formatters",
        "handlers",
        "loggers",
        "root",
    )

    def __init__(self: Self, base_folder: Path, folder_name: str = "logs", **kwargs: Any) -> None:
        self.base_folder: Path = base_folder / folder_name

        self.files: dict[str, Path] = {
            "console": self.base_folder / "console.log",
            "access": self.base_folder / "access.log",
            "sql": self.base_folder / "sql.log",
        }
        self.files.update(kwargs.get("files", {}))

        self.formatters: dict[str, Any] = FORMATTERS
        self.formatters.update(kwargs.get("formatters", {}))

        self.handlers: dict[str, Any] = {
            "stdout": {
                "formatter": "console",
                "class": HANDLER["stream"],
                "stream": "ext://sys.stdout",
            },
            "stderr": {
                "formatter": "console",
                "class": HANDLER["stream"],
                "stream": "ext://sys.stderr",
            },
            "consolelog": {
                "formatter": "file",
                "class": HANDLER["file"],
                "filename": self.files["console"],
                "when": "D",
                "delay": True,
                "backupCount": 5,
                "encoding": "utf8",
            },
            "sqllog": {
                "formatter": "file",
                "class": HANDLER["file"],
                "filename": self.files["sql"],
                "when": "D",
                "delay": True,
                "backupCount": 10,
                "encoding": "utf8",
            },
            "access": {"formatter": "access", "class": HANDLER["stream"], "stream": "ext://sys.stdout"},
            "access_file": {
                "formatter": "access_file",
                "class": HANDLER["file"],
                "filename": self.files["access"],
                "when": "D",
                "delay": True,
                "backupCount": 5,
                "encoding": "utf8",
            },
        }
        self.handlers.update(kwargs.get("handlers", {}))

        self.loggers: dict[str, Any] = {
            "api_helper": {"level": "ERROR"},
            "api_helper.access": {
                "handlers": ["access", "consolelog", "access_file"],
                "level": "INFO",
                "propagate": False,
            },
            "api_helper.error": {"handlers": ["stderr", "consolelog"], "level": "ERROR", "propagate": False},
            "uvicorn": {"handlers": ["stderr", "consolelog"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"level": "INFO", "propagate": False},
            "sentry_sdk": {"level": "ERROR"},
            "sqlalchemy": {"handlers": ["sqllog"], "level": "INFO", "propagate": False},
            "urllib3": {"level": "INFO"},
            "httpx": {"level": "INFO"},
            "httpcore": {"level": "INFO"},
            "watchfiles": {"level": "WARNING"},
        }
        self.loggers.update(kwargs.get("loggers", {}))

        self.root: dict[str, Any] = {
            "handlers": ["stdout", "consolelog"],
            "level": "DEBUG" if config.is_debug() else "INFO",
        }
        self.root.update(kwargs.get("root", {}))

    @property
    def config(self: Self) -> dict[str, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": self.formatters,
            "handlers": self.handlers,
            "loggers": self.loggers,
            "root": self.root,
        }

    def setup(self: Self) -> None:
        if not Path.exists(self.base_folder):
            Path.mkdir(self.base_folder, parents=True)

        # For logfiles, input new line to indicate the start of the log
        for logfile in self.files.values():
            with Path.open(logfile, "a") as f:
                f.write("====== NEW APPLICATION START ======\n")

        root_logger: Logger = logging.root
        root_logger.setLevel(logging.INFO)

        # It means the logging config is not set, using the default config
        if len(root_logger.handlers) == 0:
            logging.config.dictConfig(self.config)
            logger.debug("Using default logging config.")
