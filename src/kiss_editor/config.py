import configparser
import os

CONFIG_PATH = os.path.expanduser("~/.kiss_editor.ini")


def load_config():
    try:
        if os.path.exists(CONFIG_PATH):
            config = configparser.ConfigParser()
            config.read(CONFIG_PATH)
    except configparser.Error:
        pass
    kiss = dict(config["kiss"]) if config.has_section("kiss") else {}
    return {"kiss": kiss}


def update_config_theme(theme_name: str):
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        try:
            config.read(CONFIG_PATH)
        except (configparser.Error, UnicodeDecodeError, PermissionError):
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
