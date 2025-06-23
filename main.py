import asyncio
import sys

import uvloop

from lantern import config
from lantern.core import start
from lantern.favorites import Favorites
from lantern.index import Index
from lantern.logger import Logger
from lantern.update import check_for_updates


def validate_config():
    if not config.AUTHOR or not config.EMAIL or not config.PATH:
        Logger.log(
            "ERROR",
            "Please fill in AUTHOR, EMAIL, and PATH in config.py before running.",
        )
        sys.exit(1)


async def entry():
    validate_config()
    await check_for_updates()

    args = sys.argv[1:]
    if args and args[0] in ("favs", "favorites"):
        fav = Favorites()
        for arg in args[1:]:
            if arg.startswith("--add=") or arg.startswith("-a="):
                qid = arg.split("=")[1]
                metadata = Index.extract_metadata(qid)
                if metadata is None:
                    Logger.log(
                        "ERROR",
                        "Could not find problem metadata in README. Make sure it's solved first.",
                    )
                    return
                fav.add(metadata)
                return
            elif arg.startswith("--remove=") or arg.startswith("-r="):
                qid = arg.split("=")[1]
                fav.remove(qid)
                return

        print("Usage:\n  lantern favs --remove=ID\n  lantern favs --add=ID")
        return

    await start()


def main():
    uvloop.install()
    asyncio.run(entry())


if __name__ == "__main__":
    main()
