from http import HTTPStatus

import orjson
import pytest
from typing_extensions import Self

from api_helper.responses import ErrorResponse
from api_helper.responses import SuccessResponse
from api_helper.responses import error_response
from api_helper.responses import success_response

from ..fixure import utctime_mock  # noqa


@pytest.mark.usefixtures("utctime_mock")
class TestResponseClass:
    def test_data_response(self: Self) -> None:
        response = SuccessResponse(data={"key": "value"})

        assert response.status_code == HTTPStatus.OK
        assert orjson.loads(response.body) == {
            "data": {"key": "value"},
            "datetime": "2021-01-01T00:00:00+00:00",
        }

    def test_empty_response(self: Self) -> None:
        response = SuccessResponse()

        assert response.status_code == HTTPStatus.OK
        assert orjson.loads(response.body) == {
            "data": "",
            "datetime": "2021-01-01T00:00:00+00:00",
        }

    def test_response_code(self: Self) -> None:
        response = SuccessResponse(status_code=HTTPStatus.NO_CONTENT)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert orjson.loads(response.body) == {
            "data": "",
            "datetime": "2021-01-01T00:00:00+00:00",
        }

    def test_error_response_key(self: Self) -> None:
        response = ErrorResponse()

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert orjson.loads(response.body) == {
            "error": "",
            "datetime": "2021-01-01T00:00:00+00:00",
        }


@pytest.mark.usefixtures("utctime_mock")
class TestResponseFunction:
    def test_success_response(self: Self) -> None:
        response = success_response()

        assert response.status_code == HTTPStatus.OK
        assert orjson.loads(response.body) == {
            "data": "success",
            "datetime": "2021-01-01T00:00:00+00:00",
        }

    def test_success_response_list(self: Self) -> None:
        response = success_response([])

        assert response.status_code == HTTPStatus.OK
        assert orjson.loads(response.body) == {
            "data": [],
            "datetime": "2021-01-01T00:00:00+00:00",
        }

    def test_success_response_dict(self: Self) -> None:
        response = success_response({})

        assert response.status_code == HTTPStatus.OK
        assert orjson.loads(response.body) == {
            "data": {},
            "datetime": "2021-01-01T00:00:00+00:00",
        }

    def test_success_error_with_error(self: Self) -> None:
        with pytest.raises(ValueError) as error:
            success_response(status_code=HTTPStatus.BAD_REQUEST)

        assert str(error.value) == "4xx and 5xx are not a success response."

    def test_error_response(self: Self) -> None:
        response = error_response()

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert orjson.loads(response.body) == {
            "error": "",
            "datetime": "2021-01-01T00:00:00+00:00",
        }

    def test_error_response_with_success(self: Self) -> None:
        with pytest.raises(ValueError) as error:
            error_response(status_code=HTTPStatus.TEMPORARY_REDIRECT)

        assert str(error.value) == "Only 4xx and 5xx are available for error response."
