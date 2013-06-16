# Copyright (c) 2013 Huan Do, http://huan.do

import ast

from also import also, AlsoMetaClass

class VariableTransformer(ast.NodeTransformer):
    def __init__(self, env):
        self.env = env

    def visit_Module(self, node):
        with self.env.Frame(node) as f:
            self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        with self.env.Frame(node) as f:
            self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        with self.env.Frame(node) as f:
            self.generic_visit(node)
        return node

    def visit_Import(self, node):
        assignments = {}
        target_elts = []
        value_elts = []

        for alias in node.names:
            if '.' in alias.name:
                old_name = alias.name[:alias.name.index('.')]
                new_name = self.env.current_frame.get_new_name(old_name)
                assignments[new_name] = old_name

        if assignments:
            for new_name, old_name in sorted(assignments.items()):
                target_elts.append(ast.Name(id=new_name, ctx=ast.Store()))
                value_elts.append(ast.Name(id=old_name, ctx=ast.Load()))
            assign_node = ast.Assign(
                targets=[ast.Tuple(elts=target_elts)],
                value=ast.Tuple(elts=value_elts))
            return [node, assign_node]
        else:
            return node
