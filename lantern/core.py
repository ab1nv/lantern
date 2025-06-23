from lantern.index import Index
from lantern.leetcode import Leetcode
from lantern.logger import Logger


async def start() -> None:
    Index.check_index()

    url = input("Enter Question URL: ").strip()

    if "leetcode.com/problems/" in url:
        await Leetcode.handle_leetcode(url)

    else:
        Logger.log("ERROR", "Please provide a valid Leetcode URL.")
