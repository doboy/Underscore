import ast

from also import also
from also import AlsoMetaClass
from underscore import base
from underscore.utils import AssignmentManager
from underscore.utils import valueOf

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
        _ConstantFinder(self.env, self._assignmentManager
                        ).visit(self.tree)
        _ConstantChanger(self.env).visit(self.tree)
        if len(self._assignmentManager.assignments):
            self._addAssignments()

    def _addAssignments(self):
        node = self._assignmentManager.assignNode()
        self.tree.body = [node] + self.tree.body

class _ConstantFinder(ast.NodeVisitor):
    __metaclass__ = AlsoMetaClass
    def __init__(self, env, assignmentManager):
        self.env = env
        self._assignmentManager = assignmentManager

    def visit(self, node):
        ast.NodeVisitor.visit(self, node)

    @also('visit_Num')
    @also('visit_Str')
    def visit_Constant(self, node):
        value = valueOf(node)
        return self.addConstant(node, value)

    def addConstant(self, node, value):
        if value not in self.env.constants:
            delc = self.env.generateNextDeclaration()
            self._assignmentManager.addAssignment(delc.name, node)
            self.env.constants[value] = delc

    def assignNode(self):
        return self._assignmentManager.assignNode()

class _ConstantChanger(ast.NodeTransformer):
    __metaclass__ = AlsoMetaClass
    def __init__(self, env):
        self.env = env

    @also('visit_Num')
    @also('visit_Str')
    def visit_Constant(self, node):
        value = valueOf(node)
        return ast.Name(id=self.env.constants[value].name)
