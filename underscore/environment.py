import ast
from underscore import declaration

class Environment(object):
    def __init__(self, tree):
        self._generator = declaration.generator()
        self.constants = {}
        self.frames = {}
        self.starred = False
        self.tree = tree

    @property
    def global_frame(self):
        return self.frames[self.tree]
        
    def generate_new_delc(self):
        return next(self._generator)

