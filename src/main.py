import argparse
from multiprocessing import Pool

from .api_formating import get_api_calls
from .util import *
from .verbose_logging import *


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
    parser.add_argument('-v', '--verbose', help='Verbose',
                        required=False, default=True, type=bool)
    parser.add_argument('-l', '--logging_level', help='Logging level ',
                        required=False, default=VerboseLoggingLevel.INFO, type=VerboseLoggingLevel)
    return vars(parser.parse_args())


def check_single_file(filename):
    code_text = open(filename).read()
    func_calls_names = get_api_calls(code_text)
    return util_validate_api_calls(filename, func_calls_names)


if __name__ == "__main__":
    args = parse_args()
    pool = Pool(args["threads"])
    VerboseLogging.set_logging(args['verbose'], args['logging_level'])

    all_file_names = util_get_files_path_by_extension(args["dir"])

    results = pool.map(check_single_file, all_file_names)

    VerboseLogging.print_info("==================================================")
    VerboseLogging.print_info("=================== RESULT =======================")
    VerboseLogging.print_info("==================================================")
    for filename, num in zip(all_file_names, results):
        VerboseLogging.print_info(num + ": " + filename)
