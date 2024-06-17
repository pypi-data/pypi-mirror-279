import logging
from pathlib import Path

from pytest_mock import MockFixture
from typing_extensions import Self

from api_helper.config import LoggerBuilder
from api_helper.config import TimedAccessFormatter


class TestFastAPIConfigWrap:
    def test_config(self: Self, tmp_path: Path) -> None:
        config: LoggerBuilder = LoggerBuilder(tmp_path)

        assert config.base_folder == tmp_path / "logs"

    def test_log_setup(self: Self, tmp_path: Path) -> None:
        config: LoggerBuilder = LoggerBuilder(tmp_path)
        config.setup()

    def test_log_mock_root_handler(self: Self, mocker: MockFixture, tmp_path: Path) -> None:
        logger_mock: logging.Logger = mocker.patch.object(logging, "root", logging.getLogger("_tmp_"))

        config: LoggerBuilder = LoggerBuilder(tmp_path)
        config.setup()

        assert logger_mock


class TestFastAPIFormatter:
    def test_timed_access_formatter(self: Self) -> None:
        formatter: TimedAccessFormatter = TimedAccessFormatter()
        result_03: str = formatter.get_color_time(0.3)
        result_05: str = formatter.get_color_time(0.5)
        result_07: str = formatter.get_color_time(0.7)
        result_10: str = formatter.get_color_time(1.0)
        result_11: str = formatter.get_color_time(1.1)

        assert result_03 == "\x1b[32m0.300000\x1b[0m"
        assert result_05 == "\x1b[33m0.500000\x1b[0m"
        assert result_07 == "\x1b[31m0.700000\x1b[0m"
        assert result_10 == "\x1b[91m1.000000\x1b[0m"
        assert result_11 == "\x1b[91m1.100000\x1b[0m"

    def test_message(self: Self) -> None:
        formatter: TimedAccessFormatter = TimedAccessFormatter()

        record: logging.LogRecord = logging.LogRecord(
            name="test",
            level=20,
            pathname="test",
            lineno=1,
            msg="test",
            args=("localhost", "GET", "/test", "HTTP/1.1", 200, 0.5, 0),
            exc_info=None,
        )
        record.message = "test"
        message: str = formatter.formatMessage(record)
        assert message == "test"

        record: logging.LogRecord = logging.LogRecord(
            name="test",
            level=20,
            pathname="test",
            lineno=1,
            msg="test",
            args=("localhost", "GET", "/test", "HTTP/1.1", 200),
            exc_info=None,
        )
        record.message = "5word"
        message: str = formatter.formatMessage(record)
        assert message == "5word"
