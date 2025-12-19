import aiohttp
from typing import Optional, Dict


class LeetCodeClient:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://leetcode.com",
            "Referer": "https://leetcode.com/",
        }

    async def fetch_problem_data(
        self, session: aiohttp.ClientSession, question_slug: str
    ) -> Optional[Dict]:
        graphql_url = "https://leetcode.com/graphql"
        query = {
            "query": """
            query getQuestionDetails($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionFrontendId
                    title
                    difficulty
                    topicTags { name }
                }
            }""",
            "variables": {"titleSlug": question_slug},
        }

        try:
            async with session.post(
                graphql_url, json=query, headers=self.headers
            ) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                if "data" not in data or not data["data"].get("question"):
                    return None

                question = data["data"]["question"]
                return {
                    "question_id": question["questionFrontendId"],
                    "question_title": question["title"],
                    "question_slug": question_slug,
                    "difficulty": question["difficulty"],
                    "topic_tags": ", ".join(
                        tag["name"] for tag in question["topicTags"]
                    ),
                }
        except Exception:
            return None

