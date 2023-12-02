import ast
from collections import deque

from parameter import *


class KeyWordVisitor(ast.NodeVisitor):
    '''
    visit arguments (parameters passed to functions)
    '''

    def __init__(self):
        self._name = []
        self.skip = True

    @property
    def name(self):
        return self._name

    def visit_Name(self, node):
        if not self.skip and node.id is not None:
            self._name.append(Parameter(node.id, ParameterType.LOCAL_PARAM))
        self.skip = False

    def visit_Constant(self, node):
        if node.value is not None:
            self._name.append(Parameter(node.value, ParameterType.LOCAL_CONST))

    def visit_keyword(self, node):
        if node.arg is not None:
            self._name.append(Parameter(node.arg, ParameterType.KEYWORD))


class FuncCallVisitor(ast.NodeVisitor):
    '''
    visit function call nodes
    '''

    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return ".".join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


# parse function calls
def get_func_calls(tree) -> list:
    func_calls = []

    # go over the tree
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            call_visitor = FuncCallVisitor()
            call_visitor.visit(node.func)
            keyword_visitor = KeyWordVisitor()
            try:
                keyword_visitor.visit(node)
                # data format: funciton_call_name: keyword arguments
                func_calls += [(call_visitor.name, keyword_visitor.name)]
            except:
                # no keyword arguments found
                func_calls += [(call_visitor.name, [])]
    return func_calls
