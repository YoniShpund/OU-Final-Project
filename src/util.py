import importlib
import os
from inspect import signature

from .verbose_logging import *


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


def util_validate_api_calls(filename: str, api_calls: list) -> dict:
    for call in api_calls:
        api, params = call.split(":")
        module = importlib.import_module(api.split("..")[0])
        attributes = api.split("..")[1].split(".")

        VerboseLogging.print_debug(call)
        package_attr = module
        for idx in range(len(attributes)):
            VerboseLogging.print_debug(package_attr)

            if attributes[-1] in dir(package_attr):
                VerboseLogging.print_debug(
                    attributes[-1] + ' found in ' + package_attr)

            package_attr = getattr(package_attr, attributes[idx])

        # import_module = api.split("..") if ".." in api else api.split(".", 1)
        # module = importlib.import_module(import_module[0])
        # func = getattr(getattr(module, import_module[1]), import_module[2]) if len(
        #     import_module) == 3 else getattr(module, import_module[1])

        # print(call)
        # print(str(func) + '(' + params + ')')
        # print(signature(func))

    return {}
