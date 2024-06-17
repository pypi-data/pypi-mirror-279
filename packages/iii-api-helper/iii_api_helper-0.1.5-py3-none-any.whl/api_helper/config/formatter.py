from copy import copy
from logging import Logger
from logging import LogRecord
from logging import getLogger

import click
from typing_extensions import Self
from uvicorn.logging import AccessFormatter
from uvicorn.logging import DefaultFormatter

logger: Logger = getLogger(__name__)

TIMEZONE_FORMAT = "%Y-%m-%d %H:%M:%S"


class TimedAccessFormatter(AccessFormatter):
    default_time_format = TIMEZONE_FORMAT

    @staticmethod
    def get_color_time(time: float) -> str:
        s: str = f"{time:.6f}"

        if time < 0.5:
            s = click.style(str(s), fg="green")
        elif time < 0.7:
            s = click.style(str(s), fg="yellow")
        elif time < 1.0:
            s = click.style(str(s), fg="red")
        else:
            s = click.style(str(s), fg="bright_red")

        return s

    def formatMessage(self: Self, record: LogRecord) -> str:  # noqa: N802
        recordcopy = copy(record)

        if len(record.args) != 7:
            return super().formatMessage(recordcopy)

        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
            time,
            response_length,
        ) = recordcopy.args  # type: ignore[misc]

        time = self.get_color_time(time) if self.use_colors else f"{time:.6f}"

        recordcopy.__dict__.update(
            {
                "run_time": time,
                "response_length": response_length,
            }
        )

        recordcopy.args = (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        )

        return super().formatMessage(recordcopy)


class ConsoleFormatter(DefaultFormatter):
    default_time_format = TIMEZONE_FORMAT
