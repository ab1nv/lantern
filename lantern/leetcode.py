import re
import os
from datetime import datetime
import aiohttp
from lantern.logger import Logger
from lantern.metadata import Metadata
from lantern.index import Index
from lantern import config
from lantern.io import IO

base_path = os.path.abspath(config.PATH)


class Leetcode:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://leetcode.com",
            "Referer": "https://leetcode.com/",
        }

    def extract_question_slug(self, url: str) -> str | None:
        match = re.search(r"problems/([^/]+)", url)
        if match:
            Logger.log("OK", f"Extracted question slug: {match.group(1)}")
            return match.group(1)
        Logger.log("ERROR", "Could not extract slug from URL.")
        return None

    async def fetch_problem_data(
        self, session: aiohttp.ClientSession, question_slug: str
    ) -> dict | None:
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
                    Logger.log(
                        "ERROR", f"GraphQL request failed with status {response.status}"
                    )
                    return None

                data = await response.json()
                if "data" not in data or not data["data"].get("question"):
                    Logger.log("ERROR", "Invalid response from Leetcode API.")
                    return None

                question = data["data"]["question"]
                Logger.log("OK", f"Fetched metadata for '{question_slug}'")
                return {
                    "question_id": question["questionFrontendId"],
                    "question_title": question["title"],
                    "question_slug": question_slug,
                    "difficulty": question["difficulty"],
                    "topic_tags": ", ".join(
                        tag["name"] for tag in question["topicTags"]
                    ),
                }
        except Exception as e:
            Logger.log("ERROR", f"Exception occurred while fetching data: {e}")
            return None

    async def get_problem_metadata(self, url: str) -> dict | None:
        question_slug = self.extract_question_slug(url)
        if not question_slug:
            return None

        async with aiohttp.ClientSession() as session:
            return await self.fetch_problem_data(session, question_slug)

    @classmethod
    async def handle_leetcode(cls, url: str) -> None:
        instance = cls()
        metadata = await instance.get_problem_metadata(url)
        if not metadata:
            Logger.log("ERROR", "Failed to fetch problem metadata.")
            return

        slug = metadata["question_slug"]
        snake_case_slug = re.sub(r"[\W_]+", "_", slug).lower()

        folder_name = f"{metadata['question_id']}_{snake_case_slug}"
        base_path_for_problem = os.path.join(base_path, "problemset", folder_name)

        solution_file = f"{snake_case_slug}.py"
        test_file = f"test_{snake_case_slug}.py"
        readme_file = "README.md"

        IO.create_dirs(folder_name, os.path.join(base_path, "problemset"))
        IO.create_files(solution_file, base_path_for_problem)
        IO.create_files(test_file, base_path_for_problem)
        IO.create_files(readme_file, base_path_for_problem)

        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S IST")
        metadata_block = f"""Question: {metadata["question_title"]}
Solved On: {current_time}"""

        Metadata.insert_metadata(
            os.path.join(base_path_for_problem, solution_file), metadata_block, "python"
        )
        Metadata.insert_metadata(
            os.path.join(base_path_for_problem, test_file), metadata_block, "python"
        )

        solution_path = f"problemset/{folder_name}/{solution_file}"
        new_entry = (
            f"| {metadata['question_id']} "
            f"| [{metadata['question_title']}]({url}) "
            f"| [Python]({solution_path}) "
            f"| {metadata['topic_tags']} "
            f"| {metadata['difficulty']} |"
        )
        Index.insert_entry(new_entry)
