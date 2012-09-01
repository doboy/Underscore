import ast
import helpers
from collections import defaultdict

class Declaration(object):
    def __init__(self, name):
        self.name = name
        self.global_ = False
    
    @staticmethod
    def generateDeclaration():
        _ = '_'
        while True:
            yield Declaration(_)
            _ += '_'

    def __hash__(self):
        return len(self.name) * 2 + self.global_

    def __eq__(self, other):
        return self.global_ == other.global_ and \
            self.name == other.name
    

class Environment(object):
    def __init__(self, tree):
        self._generator = Declaration.generateDeclaration()
        self._global_frame = Frame(env=self)
        self._tree = tree
        
    def generateNextDeclaration(self):
        return self._generator.next()

class Frame(object):
    def __init__(self, parent=None, env=None):
        if parent is not None:
            self.parent = parent
            self.env = parent.env
        elif env is not None:
            self.parent = None
            self.env = env
        else:
            raise ValueError('Invalid argument combintation')
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
                declaration = frame.env._global_frame[name]
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
