
from enum import Enum

from termcolor import colored


class VerboseLoggingLevel(Enum):
    def __le__(self, b):
        return self.value <= b.value

    def __ge__(self, b):
        return self.value >= b.value

    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4


class VerboseLogging:

    def __init__(self, verbose: bool, logging_level: VerboseLoggingLevel) -> None:
        self.VERBOSE = verbose
        self.VERBOSE_LEVEL = logging_level

    def __print_verbose(self, msg: str) -> None:
        if (self.VERBOSE):
            print(msg)

    def print_debug(self, msg: str) -> None:
        if (self.VERBOSE_LEVEL >= VerboseLoggingLevel.DEBUG):
            self.__print_verbose(colored("[debug] " + msg, "blue"))

    def print_info(self, msg: str) -> None:
        if (self.VERBOSE_LEVEL >= VerboseLoggingLevel.INFO):
            self.__print_verbose(colored("[info] " + msg))

    def print_warn(self, msg: str) -> None:
        if (self.VERBOSE_LEVEL >= VerboseLoggingLevel.WARN):
            self.__print_verbose(colored("[warn] " + msg, 'yellow'))

    def print_error(self, msg: str) -> None:
        if (self.VERBOSE_LEVEL >= VerboseLoggingLevel.ERROR):
            self.__print_verbose(colored("[error] " + msg, 'red'))

    def print_results(self, error_msg: str, warn_msg: str, rest_msg: str):
        self.__print_verbose(
            f"{colored(error_msg, 'red')}, {colored(warn_msg, 'yellow')} {colored(rest_msg)}")
