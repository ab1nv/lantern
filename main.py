import asyncio
import uvloop

from lantern.core import start
from lantern.update import check_for_updates


async def start_lantern():
    await check_for_updates()
    await start()


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(start_lantern())
