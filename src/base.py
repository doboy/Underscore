import ast

from also import AlsoMetaClass
from underscore.frame import FRAMES
from underscore.utils import FrameContextManager

class BaseVisitor(object):
    __metaclass__ = AlsoMetaClass
        
    def __init__(self, env):
        self.env = env
        self._current_frame = None

    @property
    def _frames(self):
        return self.env.frames

    def Frame(self, node):
        self._current_frame = frame = self._frames[node]
        return FrameContextManager(frame, self)

    def extend_frame(self, node):
        assert node not in self._frames
        FrameConstructor = FRAMES[type(node)]
        frame = FrameConstructor(node, self._current_frame, self.env)
        self._frames[node] = frame
        return FrameContextManager(frame, self)

    def withdraw_frame(self):
        self._current_frame = self._current_frame.parent


