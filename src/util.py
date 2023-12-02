import importlib
import inspect
import os
from inspect import _ParameterKind, signature

from parameter import *
from pdda import logger
from verbose_logging import *

CONVENTIONAL_ALLOWED_PARAMS = ["self"]


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

    logger.print_info(
        "==================================================")
    logger.print_info(f"Analyzing - {filename}")

    error_count = 0
    for api, params in api_calls:
        inner_error_count = 0
        try:
            logger.print_info(f"Checking API - {api.split('..')[0]}")

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

            inner_error_count = _analyze_parameters(api, params, sig)

            if inner_error_count > 0:
                error_count += inner_error_count
                continue

        except Exception as _:
            logger.print_warn(
                f"API is probably built-in function (or private implementation) and cannot get signature")

    return error_count


def _analyze_parameters(api: str, params: list, sig: signature) -> int:
    inner_error_count = 0

    one_asterisk = len([1 for param in sig.parameters.values()
                        if param.kind == _ParameterKind.VAR_POSITIONAL]) > 0
    two_asterisk = len([1 for param in sig.parameters.values()
                       if param.kind == _ParameterKind.VAR_KEYWORD]) > 0

    for p in params:
        if p.type == ParameterType.KEYWORD and p.name not in sig.parameters \
            and not one_asterisk and not two_asterisk:
            inner_error_count += 1
            logger.print_error(
                f"The parameter [{p}] is not present in the signature {api}{str(sig)}")

    keyword_names = [
        p.name for p in params if p.type == ParameterType.KEYWORD]
    sig_values = [elem for elem in sig.parameters.values()
                  if elem.name not in CONVENTIONAL_ALLOWED_PARAMS]
    logger.print_debug(f"params = {params}")
    logger.print_debug(f"sig_values = {sig_values}")
    for idx, param in enumerate(sig_values):
        if param.kind == _ParameterKind.VAR_POSITIONAL \
                or param.kind == _ParameterKind.VAR_KEYWORD:
            # this param is a variadic
            continue

        if param.kind == _ParameterKind.POSITIONAL_ONLY \
                and not _validate_positional(idx, params):

            inner_error_count += 1
            logger.print_error(
                f"The {param.kind.description} parameter [{param.name}] is not present in the API call - {api}")

        elif param.kind == _ParameterKind.POSITIONAL_OR_KEYWORD \
            and not _validate_keyword(param, keyword_names) \
                and not _validate_positional(idx, params):
            inner_error_count += 1
            logger.print_error(
                f"The {param.kind.description} parameter [{param.name}] is not present in the API call - {api}")

        elif param.kind == _ParameterKind.KEYWORD_ONLY \
                and not _validate_keyword(param, keyword_names):
            inner_error_count += 1
            logger.print_error(
                f"The {param.kind.description} parameter [{param.name}] is not present in the API call - {api}")

    return inner_error_count


def _validate_positional(idx: int, params: list[Parameter]) -> bool:
    return idx < len(params) \
        and params[idx].type in [ParameterType.LOCAL_CONST, ParameterType.LOCAL_PARAM]


def _validate_keyword(param: inspect.Parameter, keyword_names: list[str]) -> bool:
    return param.name in keyword_names or param.default is not inspect.Parameter.empty
