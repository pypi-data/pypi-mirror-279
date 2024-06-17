import time
import traceback
import typing as t
from http import HTTPStatus
from logging import Logger
from logging import getLogger

from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from typing_extensions import Self
from uvicorn.protocols.utils import get_client_addr
from uvicorn.protocols.utils import get_path_with_query_string

from . import config
from .responses import error_response

logger: Logger = getLogger(__name__)

UNKNOWN_ERROR_CODE: int = HTTPStatus.INTERNAL_SERVER_ERROR
UNKNOWN_ERROR_DESCRIPTION: str = "An unknown internal error has occurred while processing the request."


class LogRequestMiddleware(BaseHTTPMiddleware):
    def __init__(
        self: Self,
        app: ASGIApp,
    ) -> None:
        super().__init__(app)

    async def dispatch(self: Self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # process the request and get the response
        start_time: float = time.time()

        try:
            response: Response = await call_next(request)

        except Exception as e:  # noqa: BLE001
            content: dict[str, t.Any] = {
                "code": UNKNOWN_ERROR_CODE,
                "detail": UNKNOWN_ERROR_DESCRIPTION,
                "parameters": {
                    "arguments": e.args,
                },
            }

            if config.is_debug():
                content["parameters"]["traceback"] = traceback.format_exc().split("\n")

            response = error_response(
                data=content,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

            self.log_error(request, response)

        process_time: float = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)
        response.background = BackgroundTask(
            self.log_time,
            request,
            response,
            process_time,
        )

        return response

    @staticmethod
    def log_error(request: Request, response: Response) -> None:
        service_logger: Logger = getLogger("api_helper.error")

        service_logger.info(
            '%s - "%s %s HTTP/%s" %d',
            get_client_addr(request.scope),  # type: ignore
            request.scope["method"],
            get_path_with_query_string(request.scope),  # type: ignore
            request.scope["http_version"],
            response.status_code,
        )
        service_logger.error(
            "Error in ASGI application",
            exc_info=True,
        )

    @staticmethod
    def log_time(request: Request, response: Response, _time: float) -> None:
        access_log: Logger = getLogger("api_helper.access")

        access_log.info(
            '%s - "%s %s HTTP/%s" %d, response time: %f, response bytes: %s',
            get_client_addr(request.scope),  # type: ignore
            request.scope["method"],
            get_path_with_query_string(request.scope),  # type: ignore
            request.scope["http_version"],
            response.status_code,
            _time,
            response.headers.get("Content-Length", 0),
        )
