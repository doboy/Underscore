import ast
from collections import defaultdict

class Frame(object):
    def __init__(self, node, parent, env):
        self.parent = parent
        self.env = env
        self._node = node
        self.declarations = {}

    def add(self, name, global_=False, conditional=False):
        if name not in self.declarations:
            self.declarations[name] = self.env.generate_new_delc()
        decl = self.declarations[name]
        decl.global_ |= global_
        if decl._conditional is None:
            decl._conditional = conditional
        else:
            decl._conditional &= conditional

    def get_new_name(self, name):
        delc = self.get_delc(name)
        return delc.name if delc else None            
        
    def get_delc(self, name):
        frame = self._lookup(name)
        if frame:
            declaration = frame.declarations[name]
            if declaration.global_:
                declaration = frame.env.global_frame.declarations[name]
            return declaration
        
    def _lookup(current_frame, name):
        """Returns the environment that contains the defintion of name."""
        while current_frame is not None:
            if name in current_frame.declarations:
                return current_frame
            else:
                current_frame = current_frame.parent

    @property
    def unconditional_delcs(self):
        return [(name, delc) for (name, delc) in self.declarations.items()
                if not delc.conditional]

    @property
    def delc_assignment_node(self):
        if len(self.unconditional_delcs):
            target_elts = []
            value_elts = []
            for name, delc in sorted(self.unconditional_delcs):
                target_elts.append(ast.Name(id=name, ctx=ast.Load()))
                value_elts.append(ast.Name(id=delc.name, ctx=ast.Store()))
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
