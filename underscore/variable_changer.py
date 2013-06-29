# Copyright (c) 2013 Huan Do, http://huan.do

import ast

from also import also, AlsoMetaClass

from assignment_manager import AssignmentManager

class VariableChanger(ast.NodeVisitor):
    __metaclass__ = AlsoMetaClass

    def __init__(self, env):
        self.env = env
        self.assignment_manager = AssignmentManager()

    def get_new_name(self, old_name, is_imported=False):
        assert isinstance(old_name, str), str(old_name)

        new_name = (self.env.current_frame.get_new_name(old_name) or
                    self.assignment_manager.get_new_name(old_name))

        if new_name is None and self.env.starred:
            return old_name

        if new_name is None:
            new_name = self.env.generate_new_decl().name
            if not is_imported:
                self.assignment_manager.add_assignment(
                    new_name, ast.Name(id=old_name, ctx=ast.Store()))
        return new_name

    def scope_generators(self, exprs, generators):
        if generators:
            first, rest = generators[0], generators[1:]
            with self.env.Frame(first):
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
        with self.env.Frame(node) as f:
            self.generic_visit(node)
            if f.decl_assignment_node:
                node.body.append(f.decl_assignment_node)

    def visit_ClassDef(self, node):
        node.name = self.get_new_name(node.name)
        with self.env.Frame(node) as f:
            self.generic_visit(node)
            if f.decl_assignment_node:
                node.body.append(f.decl_assignment_node)

    def visit_Lambda(self, node):
        with self.env.Frame(node) as f:
            self.generic_visit(node)

    def visit_FunctionDef(self, node):
        node.name = self.get_new_name(node.name)
        with self.env.Frame(node) as f:
            self.generic_visit(node)

    def visit_Call(self, node):
        self.generic_rename(node.func)

        for arg in node.args:
            if isinstance(arg, ast.Name):
                self.generic_rename(arg)
            else:
                self.generic_visit(arg)

    def visit_arguments(self, node):
        self.generic_rename(node)

    def visit_ImportFrom(self, node):
        if node.module != '__future__':
            for alias in node.names:
                if alias.name != '*':
                    alias.asname = self.get_new_name(alias.asname, is_imported=True)

    def visit_Import(self, node):
        for alias in node.names:
            if '.' in alias.name:
                continue
            if alias.name != '*':
                alias.asname = self.get_new_name(alias.asname, is_imported=True)

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

    def rename_arg(self, node):
        node.arg = self.get_new_name(node.arg)
        assert False, ast.dump(node)

    def rename_Subscript(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    @also('rename_List')
    def rename_Tuple(self, node):
        for element in node.elts:
            self.generic_rename(element)

x = 1
