from types import SimpleNamespace

import httpx2
import pytest

from kiss_editor.updates import get_github_version, need_update

API_URL = "https://api.github.com/repos/levk-m/kiss/releases/latest"


def test_get_github_version_returns_latest_tag(monkeypatch):
    def fake_get(url, timeout, headers):
        assert url == API_URL
        assert timeout == 3
        assert headers == {"User-Agent": "kiss/1.0"}
        return SimpleNamespace(json=lambda: {"tag_name": "v1.2.3"})

    monkeypatch.setattr(httpx2, "get", fake_get)
    assert get_github_version() == "v1.2.3"


def test_get_github_version_missing_tag_defaults(monkeypatch):
    monkeypatch.setattr(httpx2, "get", lambda *a, **k: SimpleNamespace(json=lambda: {}))
    assert get_github_version() == "v0.0.0"


@pytest.mark.parametrize(
    "exc",
    [
        httpx2.RequestError("network down"),
        httpx2.HTTPStatusError(
            "server error",
            request=httpx2.Request("GET", API_URL),
            response=httpx2.Response(500),
        ),
        ValueError("bad json"),
    ],
)
def test_get_github_version_errors_return_none(monkeypatch, exc):
    def boom(*args, **kwargs):
        raise exc

    monkeypatch.setattr(httpx2, "get", boom)
    assert get_github_version() is None


def test_need_update_true_when_github_newer():
    assert need_update("1.2.3", "1.2.4")


def test_need_update_true_when_github_major_newer():
    assert need_update("1.9.9", "2.0.0")


def test_need_update_false_when_equal():
    assert not need_update("1.2.3", "1.2.3")


def test_need_update_false_when_local_newer():
    assert not need_update("2.0.0", "1.5.5")


def test_need_update_fills_missing_segments():
    assert need_update("1.2", "1.2.1")


def test_need_update_ignores_v_prefix():
    assert need_update("v0.1.0", "v0.2.0")
