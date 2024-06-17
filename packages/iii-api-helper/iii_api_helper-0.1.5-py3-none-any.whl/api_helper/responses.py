import math
import typing as t
from http import HTTPStatus
from logging import Logger
from logging import getLogger

import arrow
import orjson
from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
from starlette.responses import Response
from typing_extensions import Self

logger: Logger = getLogger(__name__)


try:  # pragma: no cover
    from sqlalchemy.orm import DeclarativeMeta

    SQLALCHEMY_INSTALLED: bool = True

except ImportError:  # pragma: no cover
    SQLALCHEMY_INSTALLED: bool = False


def _default(obj: t.Any) -> t.Any:  # pragma: no cover
    if SQLALCHEMY_INSTALLED and isinstance(type(obj), DeclarativeMeta):
        # Return obj.__dict__ if it exists and remove the _sa_instance_state
        return {key: value for key, value in obj.__dict__.items() if not key.startswith("_")}

    if isinstance(obj, BaseModel):
        return obj.model_dump()

    if isinstance(obj, bytes):
        return obj.decode()

    raise TypeError


class ORJSONResponse(JSONResponse):
    # Override the default JSONResponse to use orjson
    # same from fastapi.responses.ORJSONResponse

    def __init__(
        self: Self,
        content: t.Any,
        status_code: int = 200,
        headers: t.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
        # Customized default to use orjson
        default: t.Callable[[t.Any], t.Any] = _default,
    ) -> None:
        self.default = default

        super().__init__(content, status_code, headers, media_type, background)

    def render(self: Self, content: t.Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY, default=self.default)


class SuccessResponse(ORJSONResponse):
    key: str = "data"

    def __init__(
        self: Self,
        data: t.Iterable[bytes] | bytes | t.Iterable[str] | str | None = None,
        *,
        status_code: int | HTTPStatus = HTTPStatus.OK,
        headers: t.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(
            self.generate_content(data),
            status_code,
            headers,
            media_type,
            background,
        )

    def generate_content(self: Self, data: t.Any) -> dict[str, t.Any]:
        if data is None:
            data = ""

        return {
            self.key: data,
            "datetime": arrow.utcnow().isoformat(),
        }


class ErrorResponse(SuccessResponse):
    key: str = "error"

    def __init__(
        self: Self,
        data: t.Iterable[bytes] | bytes | t.Iterable[str] | str | None = None,
        *,
        status_code: int | HTTPStatus = HTTPStatus.BAD_REQUEST,
        headers: t.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(
            data,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )


def success_response(
    data: t.Iterable[bytes] | bytes | t.Iterable[str] | str | BaseModel | None = None,
    *,
    status_code: int | HTTPStatus = HTTPStatus.OK,
    headers: t.Mapping[str, str] | None = None,
    media_type: str | None = None,
    background: BackgroundTask | None = None,
) -> Response:
    if math.floor(status_code / 100) in (4, 5):
        msg: str = "4xx and 5xx are not a success response."
        raise ValueError(msg)

    if data is None:
        data = "success"

    return SuccessResponse(
        data,
        status_code=status_code,
        headers=headers,
        media_type=media_type,
        background=background,
    )


def error_response(
    data: t.Iterable[bytes] | bytes | t.Iterable[str] | str | None = None,
    *,
    status_code: int | HTTPStatus = HTTPStatus.BAD_REQUEST,
    headers: t.Mapping[str, str] | None = None,
    media_type: str | None = None,
    background: BackgroundTask | None = None,
) -> Response:
    if math.floor(status_code / 100) not in (4, 5):
        msg: str = "Only 4xx and 5xx are available for error response."
        raise ValueError(msg)

    return ErrorResponse(
        data,
        status_code=status_code,
        headers=headers,
        media_type=media_type,
        background=background,
    )
