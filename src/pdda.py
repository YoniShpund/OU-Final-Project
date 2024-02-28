import argparse
from multiprocessing import Pool

from api_formating import get_api_calls
from util import *
from verbose_logging import *


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Project Dependencies Deprecations Analyzer')
    parser.add_argument('-d', '--dir', help='Porject to analyze full path',
                        required=True, type=dir_path)
    parser.add_argument('-t', '--threads', help='Number of threads',
                        required=False, default=20, type=int)
    parser.add_argument('-v', '--verbose', help='Allow all logs',
                        required=False, default=False, type=bool)
    parser.add_argument('-l', '--logging_level', help='Logging level (ERROR = 1, WARN = 2, INFO = 3, DEBUG = 4)',
                        required=False, default=VerboseLoggingLevel.INFO.value, type=int,
                        choices=range(VerboseLoggingLevel.MIN.value,
                                      VerboseLoggingLevel.MAX.value + 1),
                        metavar=f"[{VerboseLoggingLevel.MIN.value}-{VerboseLoggingLevel.MAX.value}]")
    return vars(parser.parse_args())


args = parse_args()
logger = VerboseLogging(args['verbose'], int(args['logging_level']))


def check_single_file(filename) -> tuple:
    try:
        code_text = open(filename).read()
        func_calls_names = get_api_calls(code_text)
    except Exception as _:
        return -1
    return util_validate_api_calls(filename, func_calls_names)


def main():
    pool = Pool(args["threads"])
    all_file_names = util_get_files_path_by_extension(args["dir"])

    results = pool.map(check_single_file, all_file_names)

    print("==================================================")
    print("=================== RESULT =======================")
    print("==================================================")
    for filename, num in zip(all_file_names, results):
        if num == -1:
            logger.print_error(f"Couldn't find file - {filename}")
        else:
            logger.print_results(
                str(num[0]) + " errors", str(num[1]) + " warnings", "in - " + filename)


if __name__ == "__main__":
    main()
