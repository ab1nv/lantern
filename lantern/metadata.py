import os


class Metadata:
    @classmethod
    def insert_metadata(cls, file: str, data: str, comment_style: str) -> None:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File does not exist: {file}")

        with open(file, "r", encoding="utf-8") as f:
            original_content = f.read()

        if comment_style == "python":
            commented_data = "\n".join(
                f"# {line}" for line in data.strip().splitlines()
            )
        elif comment_style == "java":
            commented_lines = "\n".join(
                f" * {line}" for line in data.strip().splitlines()
            )
            commented_data = f"/**\n{commented_lines}\n */"
        else:
            raise ValueError(f"Unsupported comment style: {comment_style}")

        with open(file, "w", encoding="utf-8") as f:
            f.write(commented_data + "\n\n" + original_content)
