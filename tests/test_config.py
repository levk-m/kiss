import builtins
import configparser

from kiss_editor import config


def _read(path):
    parser = configparser.ConfigParser()
    parser.read(path)
    return parser


def test_load_config_returns_kiss_when_file_missing(config_path):
    assert config.load_config() == {"kiss": {}}


def test_load_config_parses_valid_ini(config_path):
    config_path.write_text("[kiss]\ntheme = nord\n")
    assert config.load_config() == {"kiss": {"theme": "nord"}}


def test_load_config_returns_empty_kiss_for_foreign_sections(config_path):
    config_path.write_text("[other]\nfoo = 1\n")
    assert config.load_config() == {"kiss": {}}


def test_load_config_handles_empty_file(config_path):
    config_path.write_text("")
    assert config.load_config() == {"kiss": {}}


def test_load_config_handles_invalid_ini(config_path):
    config_path.write_text("{ not ini")
    assert config.load_config() == {"kiss": {}}


def test_load_config_handles_os_error(config_path, monkeypatch):
    config_path.write_text("[kiss]\ntheme = nord\n")

    def boom(*args, **kwargs):
        raise OSError("boom")

    monkeypatch.setattr("builtins.open", boom)
    assert config.load_config() == {"kiss": {}}


def test_load_config_coerces_bools_and_ints(config_path):
    config_path.write_text(
        "[kiss]\n"
        "theme = nord\n"
        "show_line_numbers = false\n"
        "soft_wrap = false\n"
        "highlight_cursor_line = true\n"
        "start-screen = false\n"
        "auto-close-pairs = true\n"
        "auto-update-check = true\n"
        "emoji-icons = false\n"
        "indent-size = 4\n"
    )
    assert config.load_config() == {
        "kiss": {
            "theme": "nord",
            "show_line_numbers": False,
            "soft_wrap": False,
            "highlight_cursor_line": True,
            "start-screen": False,
            "auto-close-pairs": True,
            "auto-update-check": True,
            "emoji-icons": False,
            "indent-size": 4,
        }
    }


def test_load_config_skips_invalid_bool(config_path):
    config_path.write_text("[kiss]\ntheme = nord\nshow_line_numbers = fales\n")
    assert config.load_config() == {"kiss": {"theme": "nord"}}


def test_update_config_theme_preserves_other_keys(config_path):
    config_path.write_text("[kiss]\ntheme = old\neditor-theme = css\n")
    config.update_config_theme("nord")
    parser = _read(config_path)
    assert parser.get("kiss", "theme") == "nord"
    assert parser.get("kiss", "editor-theme") == "css"


def test_update_config_theme_creates_file(config_path):
    config.update_config_theme("nord")
    parser = _read(config_path)
    assert parser.get("kiss", "theme") == "nord"


def test_update_config_theme_handles_empty_file(config_path):
    config_path.write_text("")
    config.update_config_theme("nord")
    parser = _read(config_path)
    assert parser.get("kiss", "theme") == "nord"


def test_update_config_theme_os_error_leaves_file_untouched(config_path, monkeypatch):
    config_path.write_text("[kiss]\ntheme = old\n")

    def boom(*args, **kwargs):
        raise OSError("boom")

    monkeypatch.setattr("builtins.open", boom)
    config.update_config_theme("nord")
    assert config_path.read_text() == "[kiss]\ntheme = old\n"


def test_update_config_theme_invalid_ini_no_write(config_path):
    config_path.write_text("{ not ini")
    config.update_config_theme("nord")
    assert config_path.read_text() == "{ not ini"


def test_update_config_theme_missing_theme_adds_it(config_path):
    config_path.write_text("[kiss]\neditor-theme = css\n")
    config.update_config_theme("nord")
    parser = _read(config_path)
    assert parser.get("kiss", "theme") == "nord"
    assert parser.get("kiss", "editor-theme") == "css"


def test_update_config_theme_same_theme_no_rewrite(config_path):
    config_path.write_text("[kiss]\ntheme = nord\n")
    config.update_config_theme("nord")
    assert config_path.read_text() == "[kiss]\ntheme = nord\n"


def test_update_config_theme_write_os_error_returns(config_path, monkeypatch):
    config_path.write_text("[kiss]\ntheme = old\n")
    real_open = builtins.open

    def boom_on_write(file, mode="r", *args, **kwargs):
        if mode == "w":
            raise PermissionError("denied")
        return real_open(file, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", boom_on_write)
    config.update_config_theme("nord")
    assert config_path.read_text() == "[kiss]\ntheme = old\n"
