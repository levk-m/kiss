import os
from pathlib import Path

DIR_PATH = os.path.expanduser("~/.kiss_templates")


def load_templates():
    root = Path(DIR_PATH)
    if not root.is_dir():
        return {}
    res = {}
    for path in sorted(root.iterdir()):
        if path.is_file() and not path.name.startswith("."):
            try:
                res[path.stem] = path.read_text()
            except (UnicodeDecodeError, OSError):
                continue
    return res
