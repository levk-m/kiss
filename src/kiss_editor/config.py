import json
import os

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
    try:
        with open(CONFIG_PATH, encoding="utf-8") as file:
            raw = file.read()
    except FileNotFoundError:
        raw = ""
    except OSError:
        return
    if raw.strip():
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return
    else:
        data = {}
    if not isinstance(data, dict):
        return
    kiss = data.setdefault("kiss", {})
    if kiss.get("theme") == theme_name:
        return
    kiss["theme"] = theme_name
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
