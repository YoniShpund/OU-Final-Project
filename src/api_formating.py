import ast

from func_calls_visitor import get_func_calls


# visit assignment statements - where the module imports have different name assignment
class AssignVisitor(ast.NodeVisitor):
    def __init__(self):
        self.class_obj = {}

    def visit_Assign(self, node):
        call_name = get_func_calls(node.value)
        # for an assignment and its right side has a function call
        # map this function call to its left
        if len(call_name) > 0 and isinstance(node.targets[0], ast.Name):
            self.class_obj[node.targets[0].id] = call_name[-1][0]
        return node


def get_api_ref_id(tree) -> dict:
    # key is the imported module while the value is the prefix
    func_to_full_path_dict = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_items = [module.__dict__ for module in node.names]
            for item in imported_items:
                if item['asname'] is None:
                    # alias name not found, use its imported name
                    func_to_full_path_dict[item['name']] = item['name'] + '.'
                else:
                    # otherwise, use alias name
                    func_to_full_path_dict[item['asname']] = item['name'] + '.'

        if isinstance(node, ast.ImportFrom) and node.module is not None:
            # for "import from" statements
            # module names are the head of a API name
            imported_items = [module.__dict__ for module in node.names]
            for item in imported_items:
                if item['asname'] is None:  # alias name not found
                    func_to_full_path_dict[item['name']] = node.module + \
                        '..' + item['name']
                else:
                    func_to_full_path_dict[item['asname']] = node.module + \
                        '..' + item['name']
    return func_to_full_path_dict


# formating function calls
def func_call_format(func_call_names, func_to_full_path_dict) -> list:
    result = []
    for elt in func_call_names:
        name = elt[0]
        keyword = elt[1]
        name_parts = name.split('.')
        if name_parts[0] in func_to_full_path_dict:
            full_name = func_to_full_path_dict[name_parts[0]] + \
                '.' + ".".join(name_parts[1:])
            result += [(full_name.rstrip('.'), keyword)]
        # else:
        #     result += [name + ":" + keyword]
    return result


def get_api_calls(code) -> list:
    '''
        return a list of api calls in the following format:
        <imported module>..<function name>:[param1,...]

        parameters list is optional in case there are parameters in the function call.
    '''
    try:
        tree = ast.parse(code, mode='exec')
        visitor = AssignVisitor()
        visitor.visit(tree)
        class2obj = visitor.class_obj
        func_calls_names = get_func_calls(tree)
        new_func_calls_names = []
        for name, param in func_calls_names:
            name_parts = name.split('.')  # object value
            if name_parts[0] in class2obj and len(name_parts) == 2:
                new_func_calls_names += [(class2obj[name_parts[0]] +
                                          '.' + '.'.join(name_parts[1:]), param)]
            else:
                new_func_calls_names.append((name, param))
        func_to_full_path_dict = get_api_ref_id(tree)
        func_calls_names = func_call_format(
            new_func_calls_names, func_to_full_path_dict)
    except (SyntaxError, ValueError):
        # to avoid non-python code
        func_calls_names = []

    return func_calls_names
