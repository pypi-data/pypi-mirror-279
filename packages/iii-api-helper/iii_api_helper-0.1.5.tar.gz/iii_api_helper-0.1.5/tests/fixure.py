import arrow
import pytest


@pytest.fixture()
def utctime_mock(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_utcnow() -> arrow.Arrow:
        return arrow.get("2021-01-01T00:00:00+00:00")

    monkeypatch.setattr(arrow, "utcnow", mock_utcnow)
