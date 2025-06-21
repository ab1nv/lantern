import os
import sys
from lantern.logger import Logger
from lantern import config


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
            Logger.log("ERROR", f"README.md was not found at {cls.readme_path}")
            sys.exit(0)
        Logger.log("OK", f"Found index at {cls.readme_path}")
        cls.ensure_index_format()

    @classmethod
    def generate_index(cls) -> None:
        os.makedirs(cls.base_path, exist_ok=True)
        content = cls.build_table_header()
        try:
            with open(cls.readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            Logger.log("OK", f"README.md generated at: {cls.readme_path}")
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
                    Logger.log("OK", "Index format is valid.")
                    return

                Logger.log(
                    "ERROR", "Index format missing or invalid. Inserting table header."
                )
                f.write("\n\n" + cls.build_table_header())
                Logger.log("OK", "Index table header appended to README.md.")

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

        if entry in entries:
            Logger.log("OK", "Entry already exists in README.md")
            return

        entries = [line for line in entries if line.strip() and line.count("|") >= 5]
        entries.append(entry)
        entries.sort(key=lambda x: int(x.split("|")[1].strip().lstrip("0") or "0"))

        updated_lines = pre_table + table_header + entries
        with open(cls.readme_path, "w", encoding="utf-8") as f:
            f.write("\n".join(updated_lines) + "\n")

        Logger.log("OK", "Problem setup successfully.")
