# Copyright (c) 2013 Huan Do, http://huan.do

import ast

import environment
from future_finder import FutureFinder

class FutureVisitor(object):
    def __init__(self, env):
        self.env = env
        self.tree = env.tree

    def traverse(self):
        future_finder = FutureFinder(self.env)
        future_finder.visit(self.tree)

        if future_finder.future_import_nodes:
            self.bring_nodes_to_top(future_finder.future_import_nodes)

    def bring_nodes_to_top(self, nodes):
        for node in nodes:
            self.tree.body.remove(node)
            self.tree.body = [node] + self.tree.body
