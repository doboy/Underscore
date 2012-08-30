import ast
import environment
from collections import deque

from also import AlsoMetaClass

class BaseVisitor(ast.NodeVisitor):
    __metaclass__ = AlsoMetaClass
        
    def __init__(self, env):
        self.env = env
        self._global_frame = self._current_frame = env._global_frame

    def visit(self, node):
        """Does a bfs, visit_queue will elements put inside of it 
        as it visits."""
        self.visit_queue = deque()
        ast.NodeVisitor.visit(self, node)
        while self.visit_queue:
            node = self.visit_queue.popleft()
            with self.Frame(node):
                ast.NodeVisitor.generic_visit(self, node)

    def Frame(self, node):
        self._current_frame = node._frame
        return FrameContextManager(node._frame, self)

    def extendFrame(self, node):
        assert not hasattr(node, '_frame')
        node._frame = environment.Frame(self._current_frame)
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
        self.visitor._current_frame = self.frame
    
    def __exit__(self, *_):
        self.visitor.withdrawFrame()
        
