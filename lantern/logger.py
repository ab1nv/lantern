from typing import Literal

from colorama import Fore


class Logger:
    _ERROR = Fore.RED + "[ERROR] "
    _OK = Fore.GREEN

    @classmethod
    def log(cls, log_type: Literal["ERROR", "OK"], message: str) -> None:
        log_types = {"ERROR": cls._ERROR, "OK": cls._OK}
        prefix = log_types.get(log_type, "")
        print(prefix + message)
