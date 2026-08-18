import runpy
import sys

import pytest

import kiss_editor.app as app_module


@pytest.fixture
def run_env(monkeypatch):
    calls = {"run_called": False, "theme": None}

    def fake_run(self):
        calls["run_called"] = True

    monkeypatch.setattr("kiss_editor.app.App.run", fake_run)
    monkeypatch.setattr(
        "kiss_editor.app.update_config_theme",
        lambda theme: calls.__setitem__("theme", theme),
    )
    return calls


def _run(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["kiss", *argv])
    app_module.run()


def test_run_with_directory(monkeypatch, tmp_path, run_env):
    _run(monkeypatch, str(tmp_path))
    assert run_env["run_called"] is True
    assert run_env["theme"] is not None


def test_run_with_file(monkeypatch, tmp_path, run_env):
    target = tmp_path / "hello.py"
    target.write_text("print('hi')\n")
    _run(monkeypatch, str(target))
    assert run_env["run_called"] is True


def test_run_prints_update_notice(monkeypatch, tmp_path, run_env, capsys):
    monkeypatch.setattr("kiss_editor.app.get_github_version", lambda: "v99.0.0")
    monkeypatch.setattr("kiss_editor.app.get_local_version", lambda: "v0.0.1")
    _run(monkeypatch, str(tmp_path))
    out = capsys.readouterr().out
    assert "A new version of kiss-editor is available" in out


def test_run_with_missing_path_exits(monkeypatch):
    with pytest.raises(SystemExit) as excinfo:
        _run(monkeypatch, "/nonexistent/does-not-exist")
    assert excinfo.value.code == 2


def test_run_version_exits(monkeypatch):
    with pytest.raises(SystemExit) as excinfo:
        _run(monkeypatch, "--version")
    assert excinfo.value.code == 0


def test_main_guard_runs_app(monkeypatch, tmp_path, config_path):
    calls = {"run_called": False}
    monkeypatch.setattr(sys, "argv", ["kiss", str(tmp_path)])
    monkeypatch.setattr(
        "kiss_editor.app.App.run", lambda self: calls.__setitem__("run_called", True)
    )
    runpy.run_module("kiss_editor.app", run_name="__main__")
    assert calls["run_called"] is True
