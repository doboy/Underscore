# Copyright (c) 2013 Huan Do, http://huan.do

import ast

from frame import FRAMES, ModuleFrame
from frame_context_manager import FrameContextManager
import declaration

class Environment(object):
    def __init__(self, tree):
        module_frame = ModuleFrame(
            node=tree,
            parent=None,
            env=self)

        self.frames = {
            tree: module_frame
        }

        self.current_frame = module_frame

        self.tree= tree
        self.constants = {}
        self.starred = False
        self._generator = declaration.generator()

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
