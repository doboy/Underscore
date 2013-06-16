# Copyright (c) 2013 Huan Do, http://huan.do

import ast

class Frame(object):
    def __init__(self, node, parent, env):
        self.parent = parent
        self.env = env
        self._node = node
        self.declarations = {}
        self.global_declarations = set()

    def add(self, name, is_global=False, conditional=False):
        if is_global or name in self.global_declarations:
            self.global_declarations.add(name)
            frame_containing_decl = self.env.global_frame
        else:
            frame_containing_decl = self

        if name not in frame_containing_decl.declarations:
            frame_containing_decl.declarations[name] = \
                self.env.generate_new_decl()

        decl = frame_containing_decl.declarations[name]

        if decl._conditional is None:
            decl._conditional = conditional
        else:
            decl._conditional &= conditional

    def get_new_name(self, name):
        decl = self.get_decl(name)
        return decl.name if decl else None

    def get_decl(self, name):
        frame = self._lookup(name)
        if frame:
            declaration = frame.declarations[name]
            return declaration

    def _lookup(self, name):
        """Returns the environment that contains the defintion of name."""
        current_frame = self
        while current_frame is not None:
            if name in current_frame.declarations:
                return current_frame
            else:
                current_frame = current_frame.parent

    @property
    def unconditional_decls(self):
        return [(name, decl) for (name, decl) in self.declarations.items()
                if not decl.conditional]

    @property
    def decl_assignment_node(self):
        if len(self.unconditional_decls):
            target_elts = []
            value_elts = []
            for name, decl in sorted(self.unconditional_decls):
                target_elts.append(ast.Name(id=name, ctx=ast.Load()))
                value_elts.append(ast.Name(id=decl.name, ctx=ast.Store()))
            return ast.Assign(targets=[ast.Tuple(elts=target_elts)],
                              value=ast.Tuple(elts=value_elts))

class ModuleFrame(Frame):
    pass

class ClassFrame(Frame):
    pass

class FunctionFrame(Frame):
    pass

class ComprehensionFrame(Frame):
    pass

FRAMES = { ast.FunctionDef   : FunctionFrame,
           ast.Lambda        : FunctionFrame,
           ast.ClassDef      : ClassFrame,
           ast.Module        : ModuleFrame,
           ast.comprehension : ComprehensionFrame, }
