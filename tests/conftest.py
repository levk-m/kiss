import pytest

from kiss_editor.app import Kiss


@pytest.fixture
def config_path(tmp_path, monkeypatch):
    path = tmp_path / "kiss_conf.json"
    monkeypatch.setattr("kiss_editor.config.CONFIG_PATH", str(path))
    monkeypatch.setattr("kiss_editor.app.CONFIG_PATH", str(path))
    return path


@pytest.fixture
def sample_dir(tmp_path):
    (tmp_path / "hello.py").write_text("print('hi')\n")
    (tmp_path / "notes.txt").write_text("some notes\n")
    (tmp_path / ".hidden").write_text("secret\n")
    (tmp_path / "_skip.py").write_text("skip\n")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "deep.md").write_text("# deep\n")
    return tmp_path


@pytest.fixture
async def app(config_path, tmp_path):
    the_app = Kiss(folder=tmp_path)
    async with the_app.run_test() as pilot:
        yield the_app, pilot
