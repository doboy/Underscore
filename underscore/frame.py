import ast

from collections import defaultdict


class Frame(object):
    def __init__(self, node, parent, env):
        self.parent = parent
        self.env = env
        self._node = node
        self.declarations = defaultdict(self.env.generateNextDeclaration)

    def __contains__(self, name):
        return name in self.declarations

    def __getitem__(self, name):
        return self.declarations[name]

    def add(self, name, global_=False):
        """Add a declaration into declarations, this can be down just 
        by accessing the element. If the element is not in the dict
        generateId will be called. If it is in it generateId wont be called.
        """
        self.declarations[name].global_ |= global_

    def getNewName(self, name):
        """Returns an unique id, variables scoped differently will have 
        different ids even if they have the same name. Returns None if
        we cannot find the declaration of the name, meaning either built-in, 
        (from blah import *)ed or misstyped.
        """
        try:
            frame = self._LookUpEnv(name)
            declaration = frame[name]
            if declaration.global_:
                declaration = frame.env.global_frame[name]
            return declaration.name
        except TypeError as e:
            pass

    def _LookUpEnv(current_env, name):
        """Returns the environment that contains the defintion of name."""
        while current_env is not None:
            if name in current_env:
                return current_env
            else:
                current_env = current_env.parent

    def declarationsAssignNode(self):
        if len(self.declarations):
            target_elts = []
            value_elts = []
            for name, delc in sorted(self.declarations.items()):
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

FRAMES = { ast.FunctionDef : FunctionFrame,
           ast.ClassDef    : ClassFrame,
           ast.Module      : ModuleFrame }
