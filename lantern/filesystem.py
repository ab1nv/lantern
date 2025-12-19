import re
from pathlib import Path
from typing import Dict, List, Tuple


class FileSystemManager:
    def __init__(self, root: Path):
        self.root = root
        self.solutions_folder = None
        self.readme_path = None

    def initialize(self):
        from lantern.utils import ensure_solutions_folder, ensure_readme
        
        self.solutions_folder = ensure_solutions_folder(self.root)
        self.readme_path = ensure_readme(self.root)

    def get_question_folder(self, question_id: str, question_slug: str) -> Path:
        folder_name = f"{question_id}-{question_slug}"
        return self.solutions_folder / folder_name

    def ensure_question_folder(self, question_id: str, question_slug: str) -> Path:
        from lantern.utils import format_question_id
        
        formatted_id = format_question_id(question_id)
        folder = self.get_question_folder(formatted_id, question_slug)
        folder.mkdir(exist_ok=True)
        return folder

    def ensure_question_readme(self, folder: Path, problem_data: Dict):
        readme = folder / "README.md"
        if not readme.exists():
            content = f"# {problem_data['question_id']}. {problem_data['question_title']}\n\n"
            content += f"**Difficulty:** {problem_data['difficulty']}\n\n"
            content += f"**Tags:** {problem_data['topic_tags']}\n\n"
            content += f"**Link:** https://leetcode.com/problems/{problem_data['question_slug']}/\n"
            readme.write_text(content)

    def ensure_solution_file(self, folder: Path, language: str):
        from lantern.utils import get_language_extension
        
        ext = get_language_extension(language)
        solution_file = folder / f"solution.{ext}"
        if not solution_file.exists():
            solution_file.write_text("")

    def find_table_in_readme(self) -> Tuple[int, int]:
        content = self.readme_path.read_text()
        lines = content.split("\n")
        
        table_start = -1
        table_end = -1
        
        for i, line in enumerate(lines):
            if re.search(r"#.*Title.*Solution.*Tags.*Difficulty", line, re.IGNORECASE):
                table_start = i
                break
        
        if table_start == -1:
            return -1, -1
        
        for i in range(table_start + 1, len(lines)):
            if not lines[i].strip().startswith("|") or lines[i].strip() == "":
                table_end = i
                break
        
        if table_end == -1:
            table_end = len(lines)
        
        return table_start, table_end

    def create_table_if_missing(self):
        start, end = self.find_table_in_readme()
        if start == -1:
            content = self.readme_path.read_text()
            if not content.endswith("\n"):
                content += "\n"
            content += "\n| # | Title | Solution | Tags | Difficulty |\n"
            content += "|:----:|:--------:|:--------:|:-------:|:----------:|\n"
            self.readme_path.write_text(content)

    def parse_table_rows(self) -> List[Dict]:
        start, end = self.find_table_in_readme()
        if start == -1:
            return []
        
        content = self.readme_path.read_text()
        lines = content.split("\n")
        
        rows = []
        for i in range(start + 2, end):
            line = lines[i].strip()
            if not line.startswith("|") or line == "":
                continue
            
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) < 5:
                continue
            
            question_id_match = re.search(r"(\d+)", parts[0])
            if not question_id_match:
                continue
            
            question_id = question_id_match.group(1)
            title_match = re.search(r"\[([^\]]+)\]\(([^\)]+)\)", parts[1])
            title = title_match.group(1) if title_match else parts[1]
            url = title_match.group(2) if title_match else ""
            
            solution_parts = []
            solution_matches = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", parts[2])
            for lang, path in solution_matches:
                solution_parts.append((lang, path))
            
            rows.append({
                "question_id": int(question_id),
                "title": title,
                "url": url,
                "solutions": solution_parts,
                "tags": parts[3],
                "difficulty": parts[4],
                "raw_line": line,
            })
        
        return rows

    def update_readme_table(self, problem_data: Dict, language: str):
        from lantern.utils import format_question_id, get_language_extension
        
        self.create_table_if_missing()
        
        question_id = int(problem_data["question_id"])
        question_slug = problem_data["question_slug"]
        formatted_id = format_question_id(problem_data["question_id"])
        folder = self.get_question_folder(formatted_id, question_slug)
        relative_path = folder.relative_to(self.root) / f"solution.{get_language_extension(language)}"
        relative_path_str = str(relative_path).replace("\\", "/")
        
        rows = self.parse_table_rows()
        
        existing_row = None
        for row in rows:
            if row["question_id"] == question_id:
                existing_row = row
                break
        
        if existing_row:
            solutions = existing_row["solutions"]
            lang_name = language.capitalize()
            if lang_name == "Cpp":
                lang_name = "C++"
            
            solution_exists = any(lang == lang_name for lang, _ in solutions)
            if not solution_exists:
                solutions.append((lang_name, f"./{relative_path_str}"))
            
            existing_row["solutions"] = solutions
            existing_row["tags"] = problem_data["topic_tags"]
            existing_row["difficulty"] = problem_data["difficulty"]
        else:
            lang_name = language.capitalize()
            if lang_name == "Cpp":
                lang_name = "C++"
            
            rows.append({
                "question_id": question_id,
                "title": problem_data["question_title"],
                "url": f"https://leetcode.com/problems/{question_slug}/",
                "solutions": [(lang_name, f"./{relative_path_str}")],
                "tags": problem_data["topic_tags"],
                "difficulty": problem_data["difficulty"],
                "raw_line": None,
            })
        
        rows.sort(key=lambda x: x["question_id"])
        
        content = self.readme_path.read_text()
        lines = content.split("\n")
        start, end = self.find_table_in_readme()
        
        new_lines = lines[:start + 2]
        for row in rows:
            formatted_id = format_question_id(str(row["question_id"]))
            title_link = f"[{row['title']}]({row['url']})"
            
            solution_links = []
            for lang, path in row["solutions"]:
                solution_links.append(f"[{lang}]({path})")
            solution_str = ", ".join(solution_links) if solution_links else "-"
            
            new_lines.append(
                f"| {formatted_id} | {title_link} | {solution_str} | {row['tags']} | {row['difficulty']} |"
            )
        
        new_lines.extend(lines[end:])
        self.readme_path.write_text("\n".join(new_lines))

