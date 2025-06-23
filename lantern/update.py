import os
import subprocess
import sys

import aiohttp

from lantern.logger import Logger

LOCAL_VERSION_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "VERSION"
)
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/ab1nv/lantern/master/VERSION"


def get_local_version() -> str:
    try:
        with open(LOCAL_VERSION_PATH, "r", encoding="utf-8") as f:
            version = f.read().strip()
            return version
    except FileNotFoundError:
        Logger.log(
            "ERROR",
            f"VERSION file not found at {LOCAL_VERSION_PATH}. Lantern cannot check updates without this file.",
        )
        return "0.0.0"
    except Exception as e:
        Logger.log("ERROR", f"Error reading VERSION file: {e}")
        return "0.0.0"


async def fetch_remote_version():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(GITHUB_VERSION_URL) as resp:
                if resp.status == 200:
                    text = (await resp.text()).strip()
                    return text
                else:
                    Logger.log(
                        "ERROR", f"Failed to fetch remote version: HTTP {resp.status}"
                    )
        except Exception as e:
            Logger.log("ERROR", f"Error fetching remote version: {e}")
    return None


def is_newer(v1: str, v2: str) -> bool:
    def parse(v):
        return tuple(int(x) for x in v.strip("v").split("."))

    return parse(v1) > parse(v2)


async def check_for_updates() -> bool:
    local = get_local_version()
    remote = await fetch_remote_version()
    if not remote:
        return False

    if is_newer(remote, local):
        Logger.log("OK", f"New version available: {remote} (local: {local})")
        choice = input("Do you want to update? [Y/n] ").strip().lower()
        if choice in ("", "y", "yes"):
            await perform_update()
        return True
    else:
        return False


async def perform_update():
    cwd = os.getcwd()
    try:
        subprocess.run(["git", "pull"], cwd=cwd, check=True)
        Logger.log("OK", "Repository updated. Please re-run the tool.")
        sys.exit(0)
    except Exception as e:
        Logger.log("ERROR", f"Update failed: {e}")
