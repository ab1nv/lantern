import os


class IO:
    @classmethod
    def create_files(cls, file: str, path: str) -> None:
        os.makedirs(path, exist_ok=True)
        full_path = os.path.join(path, file)

        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as _:
                pass

    @classmethod
    def create_dirs(cls, directory: str, path: str) -> None:
        full_dir = os.path.join(path, directory)
        os.makedirs(full_dir, exist_ok=True)
