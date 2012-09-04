import ast
from underscore import declaration

class Environment(object):
    def __init__(self, tree):
        self._generator = declaration.generator()
        self.tree = tree
        self.constants = {}

    @property
    def global_frame(self):
        return self.tree._frame
        
    def generateNextDeclaration(self):
        return self._generator.next()

