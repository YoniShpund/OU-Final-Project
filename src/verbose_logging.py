
from enum import Enum

from termcolor import colored


class VerboseLoggingLevel(Enum):
    def __le__(self, b):
        return self.value <= b

    def __ge__(self, b):
        return self.value >= b

    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4

    MIN = ERROR
    MAX = DEBUG

class VerboseLogging:

    def __init__(self, verbose: bool, logging_level: int) -> None:
        self.VERBOSE = verbose
        self.VERBOSE_LEVEL = logging_level

    def print_debug(self, msg: str) -> None:
        if (self.VERBOSE or self.VERBOSE_LEVEL >= VerboseLoggingLevel.DEBUG):
            print(colored("[debug] " + msg, "blue"))

    def print_info(self, msg: str) -> None:
        if (self.VERBOSE or self.VERBOSE_LEVEL >= VerboseLoggingLevel.INFO):
            print(colored("[info] " + msg))

    def print_warn(self, msg: str) -> None:
        if (self.VERBOSE or self.VERBOSE_LEVEL >= VerboseLoggingLevel.WARN):
            print(colored("[warn] " + msg, 'yellow'))

    def print_error(self, msg: str) -> None:
        if (self.VERBOSE or self.VERBOSE_LEVEL >= VerboseLoggingLevel.ERROR):
            print(colored("[error] " + msg, 'red'))

    def print_results(self, error_msg: str, warn_msg: str, rest_msg: str):
        print(
            f"{colored(error_msg, 'red')}, {colored(warn_msg, 'yellow')} {colored(rest_msg)}")
