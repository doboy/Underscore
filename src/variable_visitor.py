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
        _VariableCondFinder(self.env).visit(self.tree)
        _VariableChanger(self.env, self._assignmentManager
                         ).visit(self.tree)
        if len(self._assignmentManager.assignments):
            self._add_assignments()

    def _add_assignments(self):
        node = self._assignmentManager.assign_node()
        self.tree.body = [node] + self.tree.body

class _VariableFinder(ast.NodeVisitor, base.BaseVisitor):
    def __init__(self, env):
        base.BaseVisitor.__init__(self, env)
        self.visit_queue = deque()
        self._global = False
        self._conditional_stack = []
    
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
        if node.vararg:
            self.generic_declare(node.vararg)
        if node.kwarg:
            self.generic_declare(node.kwarg)

    def visit_Assign(self, node):
        for target in node.targets:
            self.generic_declare(target)
        ast.NodeVisitor.generic_visit(self, node)

    @also('visit_Lambda')
    def visit_Module(self, node):
        with self.extend_frame(node):
            self.visit_queue.append(node)
    
    @also('visit_ClassDef')
    @also('visit_FunctionDef')
    def new_scope(self, node):
        self.generic_declare(node.name)
        with self.extend_frame(node):
            self.visit_queue.append(node)

    def visit_ExceptHandler(self, node):
        if isinstance(node.name, ast.Name):
            self.generic_declare(node.name)

    def visit_For(self, node):
        self._conditional_stack.append(node)
        self.generic_declare(node.target)
        ast.NodeVisitor.generic_visit(self, node)
        assert node == self._conditional_stack.pop()

    def visit_Global(self, node):
        for name in node.names:
            self._global = True
            self.generic_declare(name)

    @also('visit_ImportFrom')
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == '*':
                self.env.starred = True
                continue
            if alias.asname is None:
                alias.asname = alias.name
            self.generic_declare(alias.asname)


    @also('visit_While')
    @also('visit_TryExcept')
    def visit_If(self, node):
         self._conditional_stack.append(node)
         self.generic_visit(node)
         assert node == self._conditional_stack.pop()
        
    def visit_With(self, node):
        if node.optional_vars:
            self.generic_declare(node.optional_vars)
        self.generic_visit(node)

    def scope_generators(self, generators):
        if generators:
            first = generators[0]
            rest = generators[1:]
            with self.extend_frame(first):
                self.visit_comprehension(first)
                self.scope_generators(rest)
                
    @also('visit_DictComp')
    @also('visit_ListComp')
    @also('visit_SetComp')
    def visit_Comprehensions(self, node):
        self.scope_generators(node.generators)

    def visit_comprehension(self, node):
        self.generic_declare(node.target)

    def generic_declare(self, target):
        specific_declare = 'declare_' + type(target).__name__
        getattr(self, specific_declare)(target)

    def declare_str(self, name):
        self._current_frame.add(name, self._global, bool(self._conditional_stack))
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

class _VariableCondFinder(ast.NodeVisitor, base.BaseVisitor):

    @also('visit_Module')
    @also('visit_ClassDef')
    @also('visit_FunctionDef')
    def new_scope(self, node):
        with self.Frame(node):
            self.generic_visit(node)

    def visit_Delete(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.notify_delete(target)

    def notify_delete(self, node):
        delc = self._current_frame.declarations.get(node.id)
        if delc:
            delc.delete = True

class _VariableChanger(ast.NodeVisitor, base.BaseVisitor):
    def __init__(self, env, assignmentManager):
        base.BaseVisitor.__init__(self, env)
        self._assignmentManager = assignmentManager

    def get_new_name(self, old_name, imported=False):
        assert isinstance(old_name, str), str(old_name)

        new_name = (self._current_frame.get_new_name(old_name) or
                    self._assignmentManager.get_new_name(old_name))

        if new_name is None and self.env.starred:
            return old_name

        if new_name is None:
            new_name = self.env.generate_new_delc().name
            if not imported:
                self._assignmentManager.add_assignment(
                    new_name, ast.Name(id=old_name, ctx=ast.Store()))
        return new_name
    
    def scope_generators(self, exprs, generators):
        if generators:
            first, rest = generators[0], generators[1:]
            with self.Frame(first):
                self.generic_visit(first)
                self.scope_generators(exprs, rest)
        else:
            for expr in exprs:
                self.visit(expr)

    @also('visit_DictComp')
    @also('visit_ListComp')
    @also('visit_SetComp')
    def visit_Comprehensions(self, node):
        if hasattr(node, 'elt'):
            self.scope_generators([node.elt], node.generators)
        else:
            self.scope_generators([node.key, node.value], node.generators)

    def visit_Assign(self, node):
        for target in node.targets:
            self.generic_rename(target)
        self.visit(node.value)

    def visit_Attribute(self, node):
        self.generic_rename(node)

    def visit_Module(self, node):
        with self.Frame(node) as f:
            self.generic_visit(node)
            if f.delc_assignment_node:
                node.body.append(f.delc_assignment_node)

    def visit_ClassDef(self, node):
        node.name = self.get_new_name(node.name)
        with self.Frame(node) as f:
            self.generic_visit(node)
            if f.delc_assignment_node:
                node.body.append(f.delc_assignment_node)

    def visit_Lambda(self, node):
        with self.Frame(node) as f:
            self.generic_visit(node)

    def visit_FunctionDef(self, node):
        node.name = self.get_new_name(node.name)
        with self.Frame(node) as f:
            self.generic_visit(node)

    def visit_arguments(self, node):
        self.generic_rename(node)

    @also('visit_ImportFrom')
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name != '*':
                alias.asname = self.get_new_name(alias.asname, imported=True)

    @also('visit_Name')
    def visit_Global(self, node):
        self.generic_rename(node)

    def generic_rename(self, target):
        specific_rename = 'rename_' + type(target).__name__
        getattr(self, specific_rename)(target)

    def rename_arguments(self, node):
        for arg in node.args:
            self.generic_rename(arg)
        if node.vararg:
            node.vararg = self.get_new_name(node.vararg)
        if node.kwarg:
            node.kwarg = self.get_new_name(node.kwarg)

    def rename_Attribute(self, node):
        if type(node.value) == ast.Name:
            self.generic_rename(node.value)
        else:
            self.generic_visit(node)

    def rename_Global(self, node):
        for i, name in enumerate(node.names):
            node.names[i] = self.get_new_name(name)

    def rename_Name(self, node):
        node.id = self.get_new_name(node.id)

    def rename_Subscript(self, node):
        ast.NodeVisitor.generic_visit(self, node)
    
    @also('rename_List')
    def rename_Tuple(self, node):
        for element in node.elts:
            self.generic_rename(element)
