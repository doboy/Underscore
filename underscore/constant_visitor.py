import ast
import base

from utils import AssignmentManager

class ConstantVisitor(object):
    """Rename all constants and takes a note of it, so that
    in the final phase we can inject an assignment node that 
    declares them. 
    """
    def __init__(self, env):
        self.env = env
        self._assignmentManager = AssignmentManager()
        
    def visit(self, tree):
        _ConstantFinder(self.env, self._assignmentManager
                        ).visit(tree)
        _ConstantChanger(self.env, self._assignmentManager
                         ).visit(tree)
        self._addAssignments()

    def _addAssignments(self):
        if len(self._assignmentManager.assignments):
            node = self._assignmentManager.assignNode()
            self.env.tree.body = [node] + self.env.tree.body

class _ConstantFinder(ast.NodeVisitor):
    def __init__(self, env, assignmentManager):
        self.env = env
        self._assignmentManager = assignmentManager

    def visit_Num(self, node):
        return self.addConstant(node, node.n)

    def visit_Str(self, node):
        return self.addConstant(node, node.s)

    def addConstant(self, node, value):
        if value not in self.constants:
            delc = self.env.generateNextDeclaration()
            self._assignmentManager.addAssignment(delc.name, node)
            self.constants[value] = delc

    def assignNode(self):
        return self._assignmentManager.assignNode()

    @property
    def constants(self):
        return self.env.constants

class _ConstantChanger(ast.NodeTransformer):
    def __init__(self, env, assignmentManager):
        self.env = env
        self._assignmentManager = assignmentManager

    def visit_Num(self, node):
        return ast.Name(id=self.constants[node.n].name)

    def visit_Str(self, node):
        return ast.Name(id=self.constants[node.s].name)

    @property
    def constants(self):
        return self.env.constants
