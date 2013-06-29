# Copyright (c) 2013 Huan Do, http://huan.do

import ast

from utils import value_of

class ConstantChanger(ast.NodeTransformer):

    def __init__(self, env):
        self.env = env

    def visit_Constant(self, node):
        if not hasattr(node, 'isdoc'):
            value = value_of(node)
            return ast.Name(id=self.env.constants[value].name)
        else:
            return node

    visit_Num = visit_Str = visit_Constant
