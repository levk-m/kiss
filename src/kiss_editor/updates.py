from importlib.metadata import version
from itertools import zip_longest

import httpx2


def get_local_version():
    return version("kiss-editor")


def get_github_version(
    url: str = "https://api.github.com/repos/levk-m/kiss/releases/latest",
):
    headers = {"User-Agent": "kiss/1.0"}
    try:
        response = httpx2.get(url, timeout=3, headers=headers)
    except (httpx2.RequestError, httpx2.HTTPStatusError, ValueError):
        return
    data = response.json()
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
