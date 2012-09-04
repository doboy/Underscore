import ast
from underscore import declaration

class Environment(object):
    def __init__(self, tree):
        self._generator = declaration.generator()
        self.tree = tree
        self.constants = {}
        self.frames = {}

    @property
    def global_frame(self):
        return self.frames[self.tree]
        
    def generateNextDeclaration(self):
        return self._generator.next()

