# Copyright (c) 2013 Huan Do, http://huan.do

import ast
from collections import deque

class VariableFinder(ast.NodeVisitor):

    def __init__(self, env):
        self.env = env
        self.visit_queue = deque()
        self._conditional_stack = []
        self._global = False

    def visit(self, node):
        """Does a bfs, visit_queue will elements put inside of it
        as it visits."""
        ast.NodeVisitor.visit(self, node)
        while self.visit_queue:
            node = self.visit_queue.popleft()
            with self.env.Frame(node):
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

    def visit_Lambda(self, node):
        with self.env.extend_frame(node):
            self.visit_queue.append(node)

    def new_scope(self, node):
        self.generic_declare(node.name)
        with self.env.extend_frame(node):
            self.visit_queue.append(node)

    visit_ClassDef = visit_FunctionDef = new_scope

    def visit_ExceptHandler(self, node):
        if isinstance(node.name, ast.Name):
            self.generic_declare(node.name)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_For(self, node):
        self._conditional_stack.append(node)
        self.generic_declare(node.target)
        ast.NodeVisitor.generic_visit(self, node)
        assert node == self._conditional_stack.pop()

    def visit_Global(self, node):
        for name in node.names:
            self._global = True
            self.generic_declare(name)
            self._global = False

    def visit_ImportFrom(self, node):
        if node.module != '__future__':
            for alias in node.names:
                if alias.name == '*':
                    self.env.starred = True
                    continue
                if alias.asname is None:
                    alias.asname = alias.name
                self.generic_declare(alias.asname)

    def visit_Import(self, node):
        for alias in node.names:
            if '.' in alias.name:
                name = alias.name[:alias.name.index('.')]
                self.env.current_frame.add(
                    name,
                    False,
                    bool(self._conditional_stack))
                continue
            if alias.asname is None:
                alias.asname = alias.name
            self.generic_declare(alias.asname)

    def visit_If(self, node):
        self._conditional_stack.append(node)
        self.generic_visit(node)
        assert node == self._conditional_stack.pop()

    visit_While = visit_TryExcept = visit_If

    def visit_With(self, node):
        # XXX: Python >= 3, each with statement can have multiple with items
        if hasattr(node, 'items'):
            for with_item in node.items:
                self.generic_visit(with_item)

        if hasattr(node, 'optional_vars'):
            self.generic_declare(node.optional_vars)

        self.generic_visit(node)

    visit_withitem = visit_With

    def scope_generators(self, generators):
        if generators:
            first = generators[0]
            rest = generators[1:]
            with self.env.extend_frame(first):
                self.visit_comprehension(first)
                self.scope_generators(rest)

    def visit_Delete(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.notify_delete(target)

    def notify_delete(self, node):
        decl = self.env.current_frame.declarations.get(node.id)
        if decl:
            decl.delete = True

    def visit_Comprehensions(self, node):
        self.scope_generators(node.generators)

    visit_DictComp = visit_ListComp = visit_SetComp = visit_Comprehensions

    def visit_comprehension(self, node):
        self.generic_declare(node.target)

    def generic_declare(self, target):
        specific_declare = 'declare_' + type(target).__name__
        getattr(self, specific_declare)(target)

    def declare_str(self, name):
        self.env.current_frame.add(
            name,
            self._global,
            bool(self._conditional_stack))

    def declare_Name(self, node):
        self.generic_declare(node.id)

    def declare_arg(self, node):
        self.generic_declare(node.arg)

    def declare_Subscript(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    declare_Attribute = declare_Subscript

    def declare_Tuple(self, node):
        for element in node.elts:
            self.generic_declare(element)

    declare_List = declare_Tuple
