# Copyright (c) 2013 Huan Do, http://huan.do

import ast

from assignment_manager import AssignmentManager
from utils import value_of

class ConstantFinder(ast.NodeVisitor):

    def __init__(self, env):
        self.env = env
        self.assignment_manager = AssignmentManager()

    def visit_Constant(self, node):
        if not hasattr(node, 'isdoc'):
            value = value_of(node)
            return self.add_constant(node, value)

    visit_Num = visit_Str = visit_Constant

    def visit_FunctionDef(self, node):
        if (isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Str)):
            node.body[0].value.isdoc = True
        self.generic_visit(node)

    visit_ClassDef = visit_FunctionDef

    def add_constant(self, node, value):
        if value not in self.env.constants and not hasattr(node, 'isdoc'):
            decl = self.env.generate_new_decl()
            self.assignment_manager.add_assignment(decl.name, node)
            self.env.constants[value] = decl

