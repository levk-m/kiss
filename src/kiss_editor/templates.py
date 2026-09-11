import configparser
import os

FILE_PATH = os.path.expanduser("~/.kiss_templates.ini")


def load_templates():
    config = configparser.ConfigParser(interpolation=None)
    try:
        if os.path.exists(FILE_PATH):
            config.read(FILE_PATH)
    except (configparser.Error, UnicodeDecodeError, OSError):
        return {}
    if not config.has_section("templates"):
        return {}
    return dict(config["templates"])
