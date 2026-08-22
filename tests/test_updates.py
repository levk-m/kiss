import urllib.request
from urllib.error import HTTPError, URLError

import pytest

from kiss_editor.updates import get_github_version, need_update

API_URL = "https://api.github.com/repos/levk-m/kiss/releases/latest"


class FakeResponse:
    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_get_github_version_returns_latest_tag(monkeypatch):
    captured = {}

    def fake_urlopen(req, timeout):
        captured["url"] = req.full_url
        captured["timeout"] = timeout
        captured["headers"] = dict(req.headers)
        return FakeResponse(b'{"tag_name": "v1.2.3"}')

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    assert get_github_version() == "v1.2.3"
    assert captured["url"] == API_URL
    assert captured["timeout"] == 3
    assert captured["headers"]["User-agent"] == "kiss/1.0"


def test_get_github_version_missing_tag_defaults(monkeypatch):
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda req, timeout: FakeResponse(b"{}"),
    )
    assert get_github_version() == "v0.0.0"


@pytest.mark.parametrize(
    "exc",
    [
        URLError("network down"),
        HTTPError(API_URL, 500, "Server Error", None, None),
    ],
)
def test_get_github_version_errors_return_none(monkeypatch, exc):
    def boom(*args, **kwargs):
        raise exc

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    assert get_github_version() is None


def test_get_github_version_bad_json_returns_none(monkeypatch):
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda req, timeout: FakeResponse(b"not json"),
    )
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
