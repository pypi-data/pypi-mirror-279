from logging import Logger
from logging import getLogger
from typing import Any

logger: Logger = getLogger(__name__)


class Singleton:
    _instance: Any = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:  # noqa: ARG003
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
