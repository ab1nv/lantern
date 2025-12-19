import re
from pathlib import Path
from typing import Optional


def extract_question_slug(url: str) -> Optional[str]:
    match = re.search(r"problems/([^/]+)", url)
    if match:
        return match.group(1)
    return None


def get_language_extension(language: str) -> str:
    extensions = {
        "python": "py",
        "go": "go",
        "java": "java",
        "cpp": "cpp",
    }
    return extensions.get(language.lower(), "py")


def format_question_id(question_id: str) -> str:
    num = int(question_id)
    return f"{num:04d}"


def find_solutions_folder(root: Path) -> Path:
    for folder_name in ["problemset", "solutions"]:
        folder = root / folder_name
        if folder.exists() and folder.is_dir():
            return folder
    return root / "problemset"


def ensure_solutions_folder(root: Path) -> Path:
    folder = find_solutions_folder(root)
    folder.mkdir(exist_ok=True)
    return folder


def ensure_readme(root: Path) -> Path:
    readme = root / "README.md"
    if not readme.exists():
        readme.write_text("# LeetCode Solutions\n\n")
    return readme

