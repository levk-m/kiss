import configparser
import os

CONFIG_PATH = os.path.expanduser("~/.kiss_editor.ini")

_BOOL_KEYS = {
    "show_line_numbers",
    "soft_wrap",
    "highlight_cursor_line",
    "start-screen",
    "auto-close-pairs",
    "auto-update-check",
    "emoji-icons",
}
_INT_KEYS = {"indent-size"}


def load_config():
    config = configparser.ConfigParser()
    try:
        if os.path.exists(CONFIG_PATH):
            config.read(CONFIG_PATH)
    except (configparser.Error, UnicodeDecodeError, OSError):
        return {"kiss": {}}
    if not config.has_section("kiss"):
        return {"kiss": {}}
    kiss = {}
    for k, val in config.items("kiss"):
        try:
            if k in _BOOL_KEYS:
                kiss[k] = config.getboolean("kiss", k)
            elif k in _INT_KEYS:
                kiss[k] = config.getint("kiss", k)
            else:
                kiss[k] = val
        except ValueError:
            continue
    return {"kiss": kiss}


def update_config_theme(theme_name: str):
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        try:
            config.read(CONFIG_PATH)
        except (configparser.Error, UnicodeDecodeError, OSError):
            return
    if config.has_section("kiss") and config.has_option("kiss", "theme"):
        if config.get("kiss", "theme") == theme_name:
            return
    if not config.has_section("kiss"):
        config.add_section("kiss")
    config.set("kiss", "theme", theme_name)
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as file:
            config.write(file)
    except (PermissionError, FileNotFoundError, OSError):
        return
