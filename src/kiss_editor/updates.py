import json
import urllib.request
from importlib.metadata import version
from itertools import zip_longest
from json import JSONDecodeError
from urllib.error import HTTPError, URLError


def get_local_version():
    return version("kiss-editor")


def get_github_version(
    url: str = "https://api.github.com/repos/levk-m/kiss/releases/latest",
):
    headers = {"User-Agent": "kiss/1.0"}
    r = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=3) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
    except (HTTPError, URLError, JSONDecodeError, UnicodeDecodeError):
        return
    version = data.get("tag_name", "v0.0.0")
    return version


def need_update(local: str, github: str) -> bool:
    l_ver = local.lstrip("v")
    g_ver = github.lstrip("v")
    loc, git = l_ver.split("."), g_ver.split(".")
    for lc, g in zip_longest(loc, git, fillvalue="0"):
        if int(g) != int(lc):
            return int(g) > int(lc)
    return False
