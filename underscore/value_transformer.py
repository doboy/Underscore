# Copyright (c) 2013 Huan Do, http://huan.do

import ast

from also import also

class VariableTransformer(ast.NodeVisitor):
    def __init__(self, env):
        self.env = env

    def visit_Import(self, node):
        assert False, ast.dump(node, 1, 1)
