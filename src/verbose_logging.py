
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

    # VERBOSE = False
    # VERBOSE_LEVEL = VerboseLoggingLevel.WARN

    def __init__(self, verbose: bool, logging_level: VerboseLoggingLevel) -> None:
        self.VERBOSE = verbose
        self.VERBOSE_LEVEL = logging_level

    # def set_logging(self, verbose: bool, logging_level: VerboseLoggingLevel):
    #     VerboseLogging.VERBOSE = verbose
    #     VerboseLogging.VERBOSE_LEVEL = logging_level

    def __print_verbose(self, msg: str) -> None:
        if (self.VERBOSE):
            print(msg)

    def print_debug(self, msg: str) -> None:
        if (self.VERBOSE_LEVEL >= VerboseLoggingLevel.DEBUG):
            self.__print_verbose(colored("[debug] ", None) + msg)

    def print_info(self, msg: str) -> None:
        if (self.VERBOSE_LEVEL >= VerboseLoggingLevel.INFO):
            self.__print_verbose(colored("[info] ", None) + msg)

    def print_warn(self, msg: str) -> None:
        if (self.VERBOSE_LEVEL >= VerboseLoggingLevel.WARN):
            self.__print_verbose(colored("[warn] ", 'yellow') + msg)

    def print_error(self, msg: str) -> None:
        if (self.VERBOSE_LEVEL >= VerboseLoggingLevel.ERROR):
            self.__print_verbose(colored("[error] ", 'red') + msg)
