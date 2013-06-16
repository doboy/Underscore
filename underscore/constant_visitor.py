# Copyright (c) 2013 Huan Do, http://huan.do

import ast

from constant_finder import ConstantFinder
from constant_changer import ConstantChanger

class ConstantVisitor(object):
    """Rename all constants and takes a note of it, so that
    in the final phase we can inject an assignment node that
    declares them.
    """
    def __init__(self, env):
        self.env = env
        self.tree = env.tree

    def traverse(self):
        constant_finder = ConstantFinder(self.env)
        constant_finder.visit(self.tree)
        ConstantChanger(self.env).visit(self.tree)

        if len(constant_finder.assignment_manager.assignments):
            assign_node = constant_finder.assignment_manager.get_assign_node()
            self.tree.body = [assign_node] + self.tree.body
