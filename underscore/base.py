import ast
import environment

from also import AlsoMetaClass

class BaseVisitor(ast.NodeVisitor):
    __metaclass__ = AlsoMetaClass

    def __init__(self, current_frame):
        self._global_frame = self._current_frame = current_frame

    def extendFrame(self, node):
        if not hasattr(node, '_frame'):
            node._frame = environment.Frame(self._current_frame)
        self._current_frame = node._frame
        return FrameContextManager(node._frame, self)

    def withdrawFrame(self):
        self._current_frame = self._current_frame.parent

    def die(self, node):
        # for debugging
        assert False, ast.dump(node)

class FrameContextManager(object):

    def __init__(self, frame, visitor):
        self.frame = frame
        self.visitor = visitor

    def __enter__(self):
        pass
    
    def __exit__(self, *_):
        self.visitor.withdrawFrame()
        
