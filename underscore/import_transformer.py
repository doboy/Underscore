import ast
o
from also import also, AlsoMetaClass

class variableTransformer(ast.NodeVisitor):
    def __init__(self, env):
        self.env = env

    def visit_Import(self, node):
        assert False, ast.dump(node, 1, 1)
