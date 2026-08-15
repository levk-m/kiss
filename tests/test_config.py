import json

from kiss_editor import config


def test_load_config_returns_kiss_when_file_missing(config_path):
    assert config.load_config() == {"kiss": {}}


def test_load_config_parses_valid_json(config_path):
    config_path.write_text(json.dumps({"kiss": {"theme": "nord"}}))
    assert config.load_config() == {"kiss": {"theme": "nord"}}


def test_load_config_defaults_kiss_for_foreign_keys(config_path):
    config_path.write_text(json.dumps({"foo": 1}))
    assert config.load_config() == {"foo": 1, "kiss": {}}


def test_load_config_empty_object(config_path):
    config_path.write_text("{}")
    assert config.load_config() == {"kiss": {}}


def test_load_config_handles_empty_file(config_path):
    config_path.write_text("")
    assert config.load_config() == {"kiss": {}}


def test_load_config_handles_invalid_json(config_path):
    config_path.write_text("{ not json")
    assert config.load_config() == {"kiss": {}}


def test_load_config_handles_os_error(config_path, monkeypatch):
    config_path.write_text("{}")

    def boom(*args, **kwargs):
        raise OSError("boom")

    monkeypatch.setattr("builtins.open", boom)
    assert config.load_config() == {"kiss": {}}


def test_update_config_theme_preserves_other_keys(config_path):
    config_path.write_text(
        json.dumps({"kiss": {"theme": "old", "editor-theme": "css"}})
    )
    config.update_config_theme("nord")
    data = json.loads(config_path.read_text())
    assert data == {"kiss": {"theme": "nord", "editor-theme": "css"}}


def test_update_config_theme_creates_file(config_path):
    config.update_config_theme("nord")
    assert json.loads(config_path.read_text()) == {"kiss": {"theme": "nord"}}


def test_update_config_theme_handles_empty_file(config_path):
    config_path.write_text("")
    config.update_config_theme("nord")
    assert json.loads(config_path.read_text()) == {"kiss": {"theme": "nord"}}
