import typing as t
from http import HTTPStatus

from fastapi import HTTPException
from fastapi import Request
from starlette.responses import Response
from typing_extensions import Self

from ..responses import error_response

DEFAULT_ERROR_CODE: int = HTTPStatus.INTERNAL_SERVER_ERROR
DEFAULT_ERROR_DESCRIPTION: str = "An unknown internal error has occurred while processing the request."


class ApplicationError(HTTPException):
    """Base exception for the application."""

    def __init__(
        self: Self,
        detail: str = "",
        *,
        status_code: int | str | HTTPStatus | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: t.Any,
    ) -> None:
        if detail == "":
            detail = DEFAULT_ERROR_DESCRIPTION

        if status_code is None:
            status_code = DEFAULT_ERROR_CODE

        self.detail = detail
        self.status_code = status_code
        self.parameters = kwargs

        super().__init__(status_code=status_code, detail=detail, headers=headers)


_T = t.TypeVar("_T", ApplicationError, Exception)


def handle_application_error(_: Request, exc: _T) -> Response:
    return error_response(
        {
            "code": exc.status_code,
            "detail": exc.detail,
            "parameters": exc.parameters,
        },
        status_code=exc.status_code,
    )
