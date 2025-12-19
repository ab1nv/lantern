import argparse
import asyncio
import sys
from pathlib import Path

import aiohttp

from lantern.filesystem import FileSystemManager
from lantern.leetcode import LeetCodeClient
from lantern.tui import run_tui
from lantern.utils import extract_question_slug


def parse_language(lang: str) -> str:
    lang_map = {
        "py": "python",
        "python": "python",
        "go": "go",
        "java": "java",
        "cpp": "cpp",
        "c++": "cpp",
    }
    return lang_map.get(lang.lower(), "python")


async def process_cli(url: str, language: str, root_dir: Path) -> None:
    slug = extract_question_slug(url)
    if not slug:
        print("Error: Invalid LeetCode URL", file=sys.stderr)
        sys.exit(1)

    fs_manager = FileSystemManager(root_dir)
    fs_manager.initialize()

    leetcode_client = LeetCodeClient()
    async with aiohttp.ClientSession() as session:
        problem_data = await leetcode_client.fetch_problem_data(session, slug)

    if not problem_data:
        print("Error: Failed to fetch problem data", file=sys.stderr)
        sys.exit(1)

    question_folder = fs_manager.ensure_question_folder(
        problem_data["question_id"], problem_data["question_slug"]
    )
    fs_manager.ensure_question_readme(question_folder, problem_data)
    fs_manager.ensure_solution_file(question_folder, language)
    fs_manager.update_readme_table(problem_data, language)

    print(f"Successfully added problem: {problem_data['question_title']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="TUI to manage Leetcode solution indexes.")
    parser.add_argument(
        "--url",
        type=str,
        help="LeetCode problem URL",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        help="Programming language (py/cpp/java/go)",
    )

    args = parser.parse_args()

    root_dir = Path.cwd()

    if args.url and args.language:
        language = parse_language(args.language)
        asyncio.run(process_cli(args.url, language, root_dir))
    elif args.url or args.language:
        print("Error: Both --url and --language must be provided for CLI mode", file=sys.stderr)
        sys.exit(1)
    else:
        run_tui(root_dir)


if __name__ == "__main__":
    main()

