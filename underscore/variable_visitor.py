import ast

from also import also
from collections import deque
from underscore import base
from underscore import environment
from underscore import frame
from underscore.utils import AssignmentManager

class VariableVisitor(object):
    def __init__(self, env):
        self.env = env
        self.tree = env.tree
        self._assignmentManager = AssignmentManager()

    def traverse(self):
        _VariableFinder(self.env).visit(self.tree)
        _VariableChanger(self.env, self._assignmentManager
                         ).visit(self.tree)
        if len(self._assignmentManager.assignments):
            self._addAssignments()

    def _addAssignments(self):
        node = self._assignmentManager.assignNode()
        self.tree.body = [node] + self.tree.body

class _VariableFinder(ast.NodeVisitor, base.BaseVisitor):
    def __init__(self, env):
        base.BaseVisitor.__init__(self, env)
        self.visit_queue = deque()
        self._global = False
    
    def visit(self, node):
        """Does a bfs, visit_queue will elements put inside of it 
        as it visits."""
        ast.NodeVisitor.visit(self, node)
        while self.visit_queue:
            node = self.visit_queue.popleft()
            with self.Frame(node):
                ast.NodeVisitor.generic_visit(self, node)

    def visit_arguments(self, node):
        for arg in node.args:
            self.generic_declare(arg)

    def visit_Assign(self, node):
        for target in node.targets:
            self.generic_declare(target)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Module(self, node):
        with self.extendFrame(node):
            self.visit_queue.append(node)
    
    @also('visit_FunctionDef')
    def visit_ClassDef(self, node):
        self.generic_declare(node.name)
        with self.extendFrame(node):
            self.visit_queue.append(node)

    def visit_ExceptHandler(self, node):
        if isinstance(node.name, ast.Name):
            self.generic_declare(node.name)

    def visit_For(self, node):
        self.generic_declare(node.target)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Global(self, node):
        for name in node.names:
            self._global = True
            self.generic_declare(name)

    @also('visit_ImportFrom')
    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname is None:
                alias.asname = alias.name
            self.generic_declare(alias.asname)

    def visit_With(self, node):
        if node.optional_vars:
            self.generic_declare(node.optional_vars)

    def generic_declare(self, target):
        specific_declare = 'declare_' + type(target).__name__
        getattr(self, specific_declare)(target)

    def declare_str(self, name):
        self._current_frame.add(name, self._global)
        self._global = False

    def declare_Name(self, node):
        self.generic_declare(node.id)

    @also('declare_Attribute')
    def declare_Subscript(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    @also('declare_List')
    def declare_Tuple(self, node):
        for element in node.elts:
            self.generic_declare(element)

class _VariableChanger(ast.NodeVisitor, base.BaseVisitor):
    def __init__(self, env, assignmentManager):
        base.BaseVisitor.__init__(self, env)
        self._assignmentManager = assignmentManager

    def getNewName(self, old_name):
        assert isinstance(old_name, str), old_name
        new_name = (self._current_frame.getNewName(old_name) or
                    self._assignmentManager.getNewName(old_name))
        if new_name is None:
            new_name = self.env.generateNextDeclaration().name
            self._assignmentManager.addAssignment(
                new_name, ast.Name(id=old_name, ctx=ast.Store()))
            return new_name
        else:
            return new_name
    
    def visit_Assign(self, node):
        for target in node.targets:
            self.generic_rename(target)
        self.visit(node.value)

    def visit_Attribute(self, node):
        self.generic_rename(node)

    def visit_Module(self, node):
        with self.Frame(node) as f:
            self.generic_visit(node)
            declAssignNode = f.declarationsAssignNode()
            if declAssignNode:
                node.body.append(declAssignNode)

    def visit_ClassDef(self, node):
        node.name = self.getNewName(node.name)
        with self.Frame(node) as f:
            self.generic_visit(node)
            declAssignNode = f.declarationsAssignNode()
            if declAssignNode:
                node.body.append(declAssignNode)

    def visit_FunctionDef(self, node):
        node.name = self.getNewName(node.name)
        with self.Frame(node) as f:
            self.generic_visit(node)

    @also('visit_ImportFrom')
    def visit_Import(self, node):
        for alias in node.names:
            assert alias.asname is not None
            alias.asname = self.getNewName(alias.asname)

    @also('visit_Name')
    def visit_Global(self, node):
        self.generic_rename(node)

    def generic_rename(self, target):
        specific_rename = 'rename_' + type(target).__name__
        getattr(self, specific_rename)(target)

    def rename_Attribute(self, node):
        if type(node.value) == ast.Name:
            self.generic_rename(node.value)
        else:
            self.generic_visit(node)

    def rename_Global(self, node):
        for i, name in enumerate(node.names):
            node.names[i] = self.getNewName(name)

    def rename_Name(self, node):
        node.id = self.getNewName(node.id)

    def rename_Subscript(self, node):
        ast.NodeVisitor.generic_visit(self, node)
    
    @also('rename_List')
    def rename_Tuple(self, node):
        for element in node.elts:
            self.generic_rename(element)
