import logging
from pathlib import Path

import httpx
import pytest
from typing_extensions import Self

from api_helper import FastAPI
from api_helper.errors import FastAPIError


class MockHttpGet:
    @staticmethod
    def is_success() -> bool:  # pragma: no cover
        return True


@pytest.fixture()
def success_httpx(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_get(*args, **kwargs) -> MockHttpGet:
        return MockHttpGet()

    monkeypatch.setattr(httpx, "get", mock_get)


class TestApplication:
    def test_fastapi_basefolder_not_exist(self: Self) -> None:
        with pytest.raises(FastAPIError) as error:
            FastAPI(base_folder=Path("not_exist"))

        assert error.match("^The base folder does not exist.*$")

    def test_fastapi(self: Self, tmp_path: Path) -> None:
        app: FastAPI = FastAPI(base_folder=tmp_path)

        assert app

    def test_fastapi_sentry_no_sentry_config(self: Self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        app: FastAPI = FastAPI(base_folder=tmp_path)

        caplog.set_level(logging.DEBUG)
        app.setup_sentry()

        assert "DSN is not provided." in caplog.text

    def test_fastapi_sentry_empty_str(self: Self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        app: FastAPI = FastAPI(base_folder=tmp_path)

        caplog.set_level(logging.DEBUG)
        app.setup_sentry("")

        assert "DSN is empty." in caplog.text

    def test_fastapi_sentry_valid_arg_config(
        self: Self, tmp_path: Path, caplog: pytest.LogCaptureFixture, success_httpx: None
    ) -> None:
        app: FastAPI = FastAPI(base_folder=tmp_path)
        app.setup_sentry("http://rAnd0mc0d3@example.local/5")

        assert "Sentry enabled." in caplog.text

    def test_fastapi_sentry_valid_kwarg_config(
        self: Self, tmp_path: Path, caplog: pytest.LogCaptureFixture, success_httpx: None
    ) -> None:
        app: FastAPI = FastAPI(base_folder=tmp_path)
        app.setup_sentry(dsn="http://rAnd0mc0d3@example.local/10")

        assert "Sentry enabled." in caplog.text
