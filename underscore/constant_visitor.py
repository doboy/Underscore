import ast

from utils import AssignmentManager
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
        self._assignmentManager = AssignmentManager()

    def traverse(self):
        ConstantFinder(self.env, self._assignmentManager
                        ).visit(self.tree)
        ConstantChanger(self.env).visit(self.tree)
        if len(self._assignmentManager.assignments):
            self._add_assignments()

    def _add_assignments(self):
        node = self._assignmentManager.assign_node()
        self.tree.body = [node] + self.tree.body
