from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from orjson import orjson
from starlette.requests import Request
from typing_extensions import Self

from api_helper.errors.app_error import ApplicationError
from api_helper.errors.app_error import handle_application_error

from ..fixure import utctime_mock  # noqa

if TYPE_CHECKING:
    from starlette.responses import Response


class TestApplicationError:
    def test_application_error(self: Self) -> None:
        exc: ApplicationError = ApplicationError()

        assert exc.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert exc.detail == "An unknown internal error has occurred while processing the request."

    def test_application_error_parameters(self: Self) -> None:
        exc: ApplicationError = ApplicationError(
            status_code=HTTPStatus.BAD_REQUEST, additional={"test": "test"}, list=[1, 2, 3]
        )

        assert exc.status_code == HTTPStatus.BAD_REQUEST
        assert exc.parameters == {"additional": {"test": "test"}, "list": [1, 2, 3]}

    def test_application_error_detail(self: Self) -> None:
        test_detail: str = "This is a test detail."
        exc: ApplicationError = ApplicationError(test_detail)

        assert exc.detail == test_detail

    @pytest.mark.usefixtures("utctime_mock")
    def test_application_handler(self: Self) -> None:
        response: Response = handle_application_error(Request({"type": "http"}), ApplicationError())

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert orjson.loads(response.body) == {
            "datetime": "2021-01-01T00:00:00+00:00",
            "error": {
                "code": 500,
                "detail": "An unknown internal error has occurred while processing the request.",
                "parameters": {},
            },
        }
