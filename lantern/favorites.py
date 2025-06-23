import json
import os

from lantern import config
from lantern.index import Index
from lantern.logger import Logger

FAV_PATH = os.path.join(os.path.abspath(config.PATH), "favorites.json")


class Favorites:
    def __init__(self):
        self.path = os.path.abspath(FAV_PATH)
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.isfile(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def add(self, metadata: dict) -> bool:
        qid = metadata["question_id"]
        if qid in self.data:
            Logger.log("OK", f"Already in favorites: {qid}")
            return False

        self.data[qid] = {
            "title": metadata["question_title"],
            "difficulty": metadata["difficulty"],
            "tags": metadata["topic_tags"],
            "slug": metadata["question_slug"],
        }
        self._save()
        Index.star_entry(qid)
        Logger.log("OK", f"Added to favorites: {qid}")
        return True

    def remove(self, qid: str) -> bool:
        if qid not in self.data:
            Logger.log("ERROR", f"Question ID not in favorites: {qid}")
            return False
        del self.data[qid]
        self._save()
        Index.unstar_entry(qid)
        Logger.log("OK", f"Removed from favorites: {qid}")
        return True
