import importlib
import os
import sys
from inspect import signature

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


def util_validate_api_calls(filename: str, api_calls: list) -> int:
    for call in api_calls:
        api, params = call.split(":")
        module = importlib.import_module(api.split("..")[0])
        attributes = api.split("..")[1].split(".")

        logger.print_debug(
            "==================================================")
        logger.print_debug(call)
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

        try:
            sig = signature(package_attr)
            logger.print_debug(str(sig))
            logger.print_debug(os.path.abspath(module.__file__))

        except Exception as e:
            logger.print_debug(
                f"{str(package_attr)} is probably built-in function and cannot get signature")

        # import_module = api.split("..") if ".." in api else api.split(".", 1)
        # module = importlib.import_module(import_module[0])
        # func = getattr(getattr(module, import_module[1]), import_module[2]) if len(
        #     import_module) == 3 else getattr(module, import_module[1])

        # print(call)
        # print(str(func) + '(' + params + ')')
        # print(signature(func))

    return 0
