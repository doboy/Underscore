import ast

import environment
from variable_finder import VariableFinder
from variable_changer import VariableChanger
from utils import AssignmentManager

class VariableVisitor(object):
    def __init__(self, env):
        self.env = env
        self.tree = env.tree
        self._assignmentManager = AssignmentManager()

    def traverse(self):
        VariableFinder(self.env).visit(self.tree)
        VariableChanger(self.env, self._assignmentManager
                         ).visit(self.tree)
        if len(self._assignmentManager.assignments):
            self._add_assignments()

    def _add_assignments(self):
        node = self._assignmentManager.assign_node()
        self.tree.body = [node] + self.tree.body
