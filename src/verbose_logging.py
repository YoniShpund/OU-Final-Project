
from enum import Enum

from termcolor import colored


class VerboseLoggingLevel(Enum):
    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4


class VerboseLogging:

    VERBOSE = False
    VERBOSE_LEVEL = VerboseLoggingLevel.WARN

    def set_logging(verbose: bool, logging_level: VerboseLoggingLevel):
        VerboseLogging.VERBOSE = verbose
        VerboseLogging.VERBOSE_LEVEL = logging_level

    def __print_verbose(msg: str) -> None:
        if (VerboseLogging.VERBOSE):
            print(msg)

    @staticmethod
    def print_debug(msg: str) -> None:
        if (VerboseLogging.VERBOSE_LEVEL == VerboseLoggingLevel.DEBUG):
            VerboseLogging.__print_verbose(colored("[debug] ", None) + msg)

    @staticmethod
    def print_info(msg: str) -> None:
        if (VerboseLogging.VERBOSE_LEVEL == VerboseLoggingLevel.INFO):
            VerboseLogging.__print_verbose(colored("[info] ", None) + msg)

    @staticmethod
    def print_warn(msg: str) -> None:
        if (VerboseLogging.VERBOSE_LEVEL == VerboseLoggingLevel.WARN):
            VerboseLogging.__print_verbose(colored("[warn] ", 'yellow') + msg)

    @staticmethod
    def print_error(msg: str) -> None:
        if (VerboseLogging.VERBOSE_LEVEL == VerboseLoggingLevel.ERROR):
            VerboseLogging.__print_verbose(colored("[error] ", 'red') + msg)
