import ast

from frame import FRAMES
from frame_context_manager import FrameContextManager
import declaration

class Environment(object):
    def __init__(self, tree):
        self._generator = declaration.generator()
        self.constants = {}
        self.frames = {}
        self.starred = False
        self.tree = tree
        self.current_frame = None

    @property
    def global_frame(self):
        return self.frames[self.tree]

    def generate_new_decl(self):
        return next(self._generator)

    @property
    def _frames(self):
        return self.frames

    def Frame(self, node):
        self.current_frame = frame = self._frames[node]
        return FrameContextManager(frame, self)

    def extend_frame(self, node):
        assert node not in self._frames
        FrameConstructor = FRAMES[type(node)]
        frame = FrameConstructor(node, self.current_frame, self)
        self._frames[node] = frame
        return FrameContextManager(frame, self)

    def withdraw_frame(self):
        self.current_frame = self.current_frame.parent
