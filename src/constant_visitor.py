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
            self._add_assignments()

    def _add_assignments(self):
        node = self._assignmentManager.assign_node()
        self.tree.body = [node] + self.tree.body

class _ConstantFinder(ast.NodeVisitor):
    __metaclass__ = AlsoMetaClass
    def __init__(self, env, assignmentManager):
        self.env = env
        self._assignmentManager = assignmentManager

    @also('visit_Num')
    @also('visit_Str')
    def visit_Constant(self, node):
        if not hasattr(node, 'isdoc'):
            value = valueOf(node)
            return self.addConstant(node, value)

    @also('visit_ClassDef')
    def visit_FunctionDef(self, node):
        if (isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Str)):
            node.body[0].value.isdoc = True
        self.generic_visit(node)

    def addConstant(self, node, value):
        if value not in self.env.constants and not hasattr(node, 'isdoc'):
            delc = self.env.generate_new_delc()
            self._assignmentManager.add_assignment(delc.name, node)
            self.env.constants[value] = delc

class _ConstantChanger(ast.NodeTransformer):
    __metaclass__ = AlsoMetaClass
    def __init__(self, env):
        self.env = env

    @also('visit_Num')
    @also('visit_Str')
    def visit_Constant(self, node):
        if not hasattr(node, 'isdoc'):
            value = valueOf(node)
            return ast.Name(id=self.env.constants[value].name)
        else:
            return node
