import inspect
from inspect import _ParameterKind, signature

from api_formating import get_api_calls
from parameter import *
from pdda import logger

CONVENTIONAL_ALLOWED_PARAMS = ["self"]


def analyze_parameters(api: str, params: list, sig: signature) -> int:
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


def analyze_module_file(module_file: str, package_attr) -> int:
    inner_error_count = 0
    code_text = open(module_file).read()
    # func_calls_names = get_api_calls(code_text)
    func_calls_names = list(dict.fromkeys([val for val, _ in get_api_calls(code_text)]))
    source_code = inspect.getsource(package_attr)

    for api in func_calls_names:
        if ("warn" in api):
            logger.print_debug(api)

            if "warn(" in source_code:
                logger.print_warn("Warning found in " + str(package_attr))
                inner_error_count += 1

    return inner_error_count
