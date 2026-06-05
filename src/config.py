import json
import os
from pathlib import Path

CONFIG_PATH = os.path.expanduser("~/.kiss_conf.json")


def load_config():
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
        else:
            data = {}
    except (json.JSONDecodeError, OSError):
        data = {}
    data.setdefault("kiss", {})
    return data


def update_config_theme(theme_name: str):
    data = load_config()
    data.setdefault("kiss", {})
    data["kiss"]["theme"] = theme_name
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file)
