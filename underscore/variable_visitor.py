# Copyright (c) 2013 Huan Do, http://huan.do

import ast

import environment
from variable_finder import VariableFinder
from variable_changer import VariableChanger
from variable_transformer import VariableTransformer

class VariableVisitor(object):
    def __init__(self, env):
        self.env = env
        self.tree = env.tree

    def traverse(self):
        VariableFinder(self.env).visit(self.tree)
        variable_changer = VariableChanger(self.env)
        variable_changer.visit(self.tree)

        VariableTransformer(self.env).visit(self.tree)
        if len(variable_changer.assignment_manager.assignments):
            assign_node = variable_changer.assignment_manager.get_assign_node()
            self.tree.body = [assign_node] + self.tree.body
