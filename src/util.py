import importlib
import os
from inspect import signature

from analyze import analyze_module_file, analyze_parameters
from pdda import logger
from verbose_logging import *


def util_get_files_path_by_extension(root_dir, flag='.py') -> list:
    paths = []
    for root, dirs, files in os.walk(root_dir):
        # skip hidden files such as git files
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for f in files:
            if f.endswith(flag):
                paths.append(os.path.join(root, f))
    return paths


def util_validate_api_calls(filename: str, api_calls: list) -> tuple:

    logger.print_info(
        "==================================================")
    logger.print_info(f"Analyzing - {filename}")

    error_count = 0
    warn_count = 0
    for api, params in api_calls:
        inner_error_count = 0
        try:
            logger.print_debug(f"Checking API - {api.split('..')[0]}")

            module = importlib.import_module(api.split("..")[0])
            attributes = api.split("..")[1].split(".")

            logger.print_debug(
                "==================================================")
            logger.print_debug(api + str(params))
            package_attr = module
            found_api = None
            for idx in range(len(attributes)):
                logger.print_debug(str(package_attr))

                if attributes[-1] in dir(package_attr):
                    logger.print_debug(
                        attributes[-1] + ' found in ' + str(package_attr))
                    found_api = package_attr

                package_attr = getattr(package_attr, attributes[idx])

            if found_api is None:
                # skip to next function call
                continue

            sig = signature(package_attr)
            logger.print_debug(str(sig))
            logger.print_debug(os.path.abspath(module.__file__))

            inner_error_count = analyze_parameters(api, params, sig)

            if inner_error_count > 0:
                error_count += inner_error_count
                break

            warn_count += analyze_module_file(
                os.path.abspath(module.__file__), package_attr)

        except Exception as _:
            logger.print_info(
                f"API ({api.split('..')[1].split('.')[-1]}) is probably built-in function (or private implementation) and cannot get signature")

    return (error_count, warn_count)
