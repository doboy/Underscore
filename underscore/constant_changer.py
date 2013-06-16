# Copyright (c) 2013 Huan Do, http://huan.do

import ast

from also import also
from also import AlsoMetaClass
from utils import value_of

class ConstantChanger(ast.NodeTransformer):
    __metaclass__ = AlsoMetaClass

    def __init__(self, env):
        self.env = env

    @also('visit_Num')
    @also('visit_Str')
    def visit_Constant(self, node):
        if not hasattr(node, 'isdoc'):
            value = value_of(node)
            return ast.Name(id=self.env.constants[value].name)
        else:
            return node
