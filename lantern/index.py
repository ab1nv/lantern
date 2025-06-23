import os

from lantern import config
from lantern.logger import Logger


class ReadmeNotFoundError(Exception):
    pass


class IndexFormatError(Exception):
    pass


class Index:
    base_path = os.path.abspath(config.PATH)
    readme_path = os.path.join(base_path, "README.md")

    EXPECTED_HEADER = "| # | Title | Solution | Tags | Difficulty |"
    EXPECTED_DIVIDER = "|:----:|:--------:|:--------:|:-------:|:----------:|"

    @classmethod
    def check_index(cls) -> None:
        if not os.path.isfile(cls.readme_path):
            Logger.log(
                "ERROR", f"README.md not found at {cls.readme_path}, generating it..."
            )
            cls.generate_index()
        cls.ensure_index_format()

    @classmethod
    def generate_index(cls) -> None:
        os.makedirs(cls.base_path, exist_ok=True)
        content = cls.build_table_header()
        try:
            with open(cls.readme_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            Logger.log("ERROR", f"Failed to write README.md: {e}")

    @classmethod
    def build_table_header(cls) -> str:
        header = "## Problem Index\n\n"
        table_header = cls.EXPECTED_HEADER + "\n"
        table_divider = cls.EXPECTED_DIVIDER + "\n"
        return header + table_header + table_divider

    @classmethod
    def ensure_index_format(cls) -> None:
        try:
            with open(cls.readme_path, "r+", encoding="utf-8") as f:
                content = f.read()
                if cls.EXPECTED_HEADER in content and cls.EXPECTED_DIVIDER in content:
                    return

                Logger.log(
                    "ERROR",
                    "Index format missing or invalid. Inserting table header...",
                )
                f.write("\n\n" + cls.build_table_header())
        except Exception as e:
            Logger.log("ERROR", f"Error ensuring index format: {e}")

    @classmethod
    def insert_entry(cls, entry: str) -> None:
        with open(cls.readme_path, "r", encoding="utf-8") as f:
            lines = [line.rstrip() for line in f]

        try:
            header_index = lines.index(cls.EXPECTED_HEADER)
            divider_index = lines.index(cls.EXPECTED_DIVIDER, header_index + 1)
        except ValueError:
            Logger.log("ERROR", "Could not find index table header in README.md.")
            return

        pre_table = lines[:header_index]
        table_header = lines[header_index : divider_index + 1]
        entries = lines[divider_index + 1 :]

        def format_line(line: str) -> str:
            parts = line.strip().split("|")
            if len(parts) < 6:
                return line
            qid = parts[1].strip().rstrip(".")
            parts[1] = f" {qid}."
            return "|".join(parts)

        entries = [
            format_line(line)
            for line in entries
            if line.strip() and line.count("|") >= 5
        ]

        entry = format_line(entry)
        if entry in entries:
            Logger.log("OK", "Entry already exists in README.md")
            return

        entries.append(entry)
        entries.sort(key=lambda x: int(x.split("|")[1].strip().rstrip(".")))

        updated_lines = pre_table + table_header + entries
        with open(cls.readme_path, "w", encoding="utf-8") as f:
            f.write("\n".join(updated_lines) + "\n")

        Logger.log("OK", "✅ Problem setup successfully.")

    @classmethod
    def star_entry(cls, qid: str) -> None:
        cls._update_star(qid, add_star=True)

    @classmethod
    def unstar_entry(cls, qid: str) -> None:
        cls._update_star(qid, add_star=False)

    @classmethod
    def _update_star(cls, qid: str, add_star: bool) -> None:
        if not os.path.isfile(cls.readme_path):
            Logger.log("ERROR", "README.md not found when trying to update star.")
            return

        try:
            with open(cls.readme_path, "r", encoding="utf-8") as f:
                lines = [line.rstrip() for line in f]

            modified = False
            for i, line in enumerate(lines):
                parts = line.strip().split("|")
                if len(parts) < 6:
                    continue
                entry_id = parts[1].strip().rstrip(".")
                if entry_id == qid:
                    if add_star and "⭐" not in parts[2]:
                        parts[2] = parts[2].replace("]", " ⭐]")
                        lines[i] = "|".join(parts)
                        modified = True
                    elif not add_star and "⭐" in parts[2]:
                        parts[2] = parts[2].replace(" ⭐", "")
                        lines[i] = "|".join(parts)
                        modified = True
                    break

            if modified:
                with open(cls.readme_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + "\n")
                Logger.log(
                    "OK",
                    f"{'Starred' if add_star else 'Unstarred'} question {qid} in README.",
                )
            else:
                Logger.log("OK", f"No change needed for {qid} in README.")
        except Exception as e:
            Logger.log("ERROR", f"Failed to update README star for {qid}: {e}")

    @classmethod
    def extract_metadata(cls, qid: str) -> dict | None:
        if not os.path.isfile(cls.readme_path):
            return None

        dot_qid = f"{qid}."

        with open(cls.readme_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) < 6:
                    continue
                entry_id = parts[1].strip()
                if entry_id == dot_qid:
                    return {
                        "question_id": qid,
                        "question_title": parts[2]
                        .split("]")[0]
                        .split("[")[-1]
                        .replace(" ⭐", ""),
                        "difficulty": parts[5].strip(),
                        "topic_tags": parts[4].strip(),
                        "question_slug": parts[3].split("/")[-1].replace(".py)", ""),
                    }

        return None
