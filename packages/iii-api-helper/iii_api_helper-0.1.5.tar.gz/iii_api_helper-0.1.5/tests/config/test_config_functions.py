import math
import os
from collections.abc import Generator
from pathlib import Path
from unittest import mock

import pytest
from typing_extensions import Self

from api_helper.config import is_debug
from api_helper.config import is_reload
from api_helper.config.configure import _auto_convert
from api_helper.config.configure import _convert_bool
from api_helper.config.configure import get
from api_helper.config.configure import load_config
from api_helper.errors import ConfigError


@pytest.fixture()
def set_debug_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    with mock.patch.dict(os.environ, clear=True):
        envvars = {
            "DEBUG": "true",
        }
        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        yield  # This is the magical bit which restore the environment after


@pytest.fixture()
def set_reload_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    with mock.patch.dict(os.environ, clear=True):
        envvars = {
            "RELOAD": "true",
        }
        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        yield  # This is the magical bit which restore the environment after


@pytest.fixture()
def set_test_envs(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    with mock.patch.dict(os.environ, clear=True):
        envvars = {
            "TEST_TRUE": "true",
            "TEST_FALSE": "false",
            "TEST_INT": "255",
            "TEST_FLOAT": "3.14",
        }
        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        yield  # This is the magical bit which restore the environment after


class TestDebug:
    def test_is_debug_default(self: Self) -> None:
        assert is_debug() is False

    def test_is_debug_set_true(self: Self, set_debug_env: None) -> None:
        assert is_debug() is True


class TestReload:
    def test_is_reload_default(self: Self) -> None:
        assert is_reload() is False

    def test_is_reload_set_true(self: Self, set_reload_env: None) -> None:
        assert is_reload() is True


class TestConvert:
    def test_convert_bool(self: Self) -> None:
        for value in ["True", "true", "1"]:
            assert _convert_bool(value) is True

        for value in ["False", "false", "0"]:
            assert _convert_bool(value) is False

    def test_convert_bool_error(self: Self) -> None:
        with pytest.raises(ConfigError) as error:
            _convert_bool("invalid")

        assert error.match("^Cannot convert.*$")


class TestAutoConvert:
    def test_convert_none(self: Self) -> None:
        assert _auto_convert(None) is None

    def test_convert_bool(self: Self) -> None:
        assert _auto_convert("true") is True
        assert _auto_convert("false") is False
        assert _auto_convert("1") is True
        assert _auto_convert("0") is False
        assert _auto_convert("yes") is True
        assert _auto_convert("no") is False

    def test_convert_int(self: Self) -> None:
        assert _auto_convert("1") == 1
        assert _auto_convert("0") == 0
        assert _auto_convert("-1") == -1

    def test_convert_float(self: Self) -> None:
        assert math.isclose(_auto_convert("1.0"), 1.0, rel_tol=1e-09, abs_tol=1e-09)
        assert math.isclose(_auto_convert("0.0"), 0.0, rel_tol=1e-09, abs_tol=1e-09)
        assert math.isclose(_auto_convert("-1.0"), -1.0, rel_tol=1e-09, abs_tol=1e-09)

    def test_convert_list(self: Self) -> None:
        assert _auto_convert("[1, 2, 3]") == [1, 2, 3]
        assert _auto_convert('["a", "b", "c"]') == ["a", "b", "c"]
        assert _auto_convert("[1, 2.0, 'c']") == [1, 2.0, "c"]

    def test_convert_dict(self: Self) -> None:
        assert _auto_convert('{"a": 1, "b": 2, "c": 3}') == {"a": 1, "b": 2, "c": 3}
        assert _auto_convert('{"a": "a", "b": "b", "c": "c"}') == {"a": "a", "b": "b", "c": "c"}
        assert _auto_convert('{"a": 1, "b": 2.0, "c": "c"}') == {"a": 1, "b": 2.0, "c": "c"}

    def test_convert_string(self: Self) -> None:
        assert _auto_convert("a") == "a"
        assert _auto_convert("b") == "b"
        assert _auto_convert("long_long_string") == "long_long_string"

    def test_convert_object(self: Self) -> None:
        with pytest.raises(ConfigError) as error:
            _auto_convert(object)

        assert error.match("^Cannot convert.*, should be a string or None.$")


class TestGet:
    def test_get_default_key(self: Self) -> None:
        assert get("key") is None
        assert get("key", None) is None
        assert get("key", "default") == "default"

    def test_get_convert(self: Self, set_test_envs: None) -> None:
        assert get("TEST_TRUE", convert=True) is True
        assert get("TEST_FALSE", convert=True) is False
        assert get("TEST_INT", convert=True) == 255
        assert math.isclose(get("TEST_FLOAT", convert=True), 3.14, rel_tol=1e-09, abs_tol=1e-09)

    def test_get_raise_error(self: Self) -> None:
        with pytest.raises(ConfigError) as error:
            get("key", raise_error=True)

        assert error.match("^Key 'key' not found.$")


class TestLoadConfig:
    def test_load_config(self: Self) -> None:
        result = load_config(Path(__file__).parent.parent / "statics/sample_env")

        assert result is None

    def test_load_config_dir(self: Self) -> None:
        Path.touch(Path(__file__).parent.parent / "statics/.env")

        result = load_config(Path(__file__).parent.parent / "statics")

        assert result is None

    def test_load_not_exist_config(self: Self) -> None:
        with pytest.raises(ConfigError) as error:
            load_config(Path("not_exist"))

        assert error.match("^The env file not_exist does not exist or is not a directory containing .env file.$")
