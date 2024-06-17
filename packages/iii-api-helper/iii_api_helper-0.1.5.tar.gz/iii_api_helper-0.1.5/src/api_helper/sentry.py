from logging import Logger
from logging import getLogger
from typing import TYPE_CHECKING
from typing import Any

import httpx
import sentry_sdk
from fastapi import FastAPI
from httpx._urlparse import ParseResult
from httpx._urlparse import urlparse
from sentry_sdk.client import _get_options

logger: Logger = getLogger(__name__)


def _init(*args: str | None, **kwargs: Any) -> None:
    """
    Initialize Sentry SDK, add the url check before initializing.
    Read sentry_sdk.init for more information.

    Args:
        *args:
        **kwargs:

    Returns:
        None
    """
    if len(args) >= 1 and issubclass(type(args[0]), FastAPI):
        args = args[1:]

    if args and isinstance(args[0], str):
        dsn: str = args[0]  # DSN is the first argument
    else:
        dsn: str = kwargs.get("dsn") or _get_options().get("dsn")

    if dsn is None:
        logger.debug("DSN is not provided.")
        return

    if dsn == "":
        logger.debug("DSN is empty.")
        return

    parse_url: ParseResult = urlparse(dsn)
    test_connection: httpx.Response = httpx.get(f"{parse_url.scheme}://{parse_url.netloc}")

    if test_connection.is_success or test_connection.is_redirect:
        sentry_sdk.init(*args, **kwargs)

        logger.info("Sentry enabled.")


# Fake sentry_init for type hinting
if TYPE_CHECKING:
    from sentry_sdk.consts import ClientConstructor
    from sentry_sdk.hub import _InitGuard

    class sentry_init(ClientConstructor, _InitGuard):  # noqa: N801
        pass
else:
    sentry_init = (lambda: _init)()
