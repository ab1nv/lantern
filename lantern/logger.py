from colorama import Fore
from typing import Literal


class Logger:
    _ERROR = Fore.RED + "[ERROR] "
    _OK = Fore.GREEN + "[OK] "

    @classmethod
    def log(cls, log_type: Literal["ERROR", "OK"], message: str) -> None:
        log_types = {"ERROR": cls._ERROR, "OK": cls._OK}
        prefix = log_types.get(log_type, "")
        print(prefix + message)
