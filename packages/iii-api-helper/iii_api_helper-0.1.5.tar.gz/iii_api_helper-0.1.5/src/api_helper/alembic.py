import sys
from io import StringIO
from logging import Logger
from logging import getLogger
from pathlib import Path
from typing import TextIO

from sqlalchemy import URL
from typing_extensions import Self

try:
    from alembic.command import current
    from alembic.command import upgrade
    from alembic.config import Config
    from alembic.script import ScriptDirectory

except ImportError:
    error_message: str = "Alembic is not installed. Run `pip install iii-api-helper[database]`"
    raise ImportError(error_message) from None

logger: Logger = getLogger(__name__)


class Alembic:
    __slots__ = ["buffer", "ini_file", "scripts", "sql_str"]

    alembic_logger: Logger = getLogger("alembic.runtime.migration")

    def __init__(self: Self, ini_file: Path | str, script_location: Path | str, sql_uri: str | URL) -> None:
        self.ini_file = Path(ini_file)
        self.scripts = Path(script_location)

        self.sql_str = str(sql_uri)

        self.buffer: TextIO | StringIO = sys.stdout

    @property
    def script_directory(self: Self) -> ScriptDirectory:
        return ScriptDirectory.from_config(self.get_config())

    @property
    def current(self: Self) -> str:
        # https://stackoverflow.com/a/61770854
        self.alembic_logger.disabled = True
        self.buffer = StringIO()

        current(self.get_config())
        _out: str = self.buffer.getvalue().strip()

        self.alembic_logger.disabled = False
        self.buffer.close()
        self.buffer = sys.stdout

        return _out[:12]

    @property
    def head(self: Self) -> str:
        return self.script_directory.get_current_head()

    @property
    def upgradeable(self: Self) -> bool:
        # noinspection PyTestUnpassedFixture
        return self.current != self.head

    def get_config(self: Self) -> Config:
        _config: Config = Config(self.ini_file, stdout=self.buffer)

        # Patch the config file for the correct database URI
        if _config.get_main_option("sqlalchemy.url") != self.sql_str:
            _config.set_main_option("sqlalchemy.url", self.sql_str)

        _config.set_main_option("script_location", f"{self.scripts}")

        return _config

    def upgrade(self: Self, version: str = "head") -> None:
        upgrade(self.get_config(), version)
