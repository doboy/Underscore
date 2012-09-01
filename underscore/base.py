import ast

from also import AlsoMetaClass
from frame import FRAMES
from utils import FrameContextManager

class BaseVisitor(object):
    __metaclass__ = AlsoMetaClass
        
    def __init__(self, env):
        self.env = env
        self._current_frame = None

    def Frame(self, node):
        self._current_frame = node._frame
        return FrameContextManager(node._frame, self)

    def extendFrame(self, node):
        assert not hasattr(node, '_frame')
        FrameConstructor = FRAMES[type(node)]
        node._frame = FrameConstructor(node, self._current_frame, self.env)
        return FrameContextManager(node._frame, self)

    def withdrawFrame(self):
        self._current_frame = self._current_frame.parent

    def die(self, node):
        # for debugging
        assert False, ast.dump(node)

