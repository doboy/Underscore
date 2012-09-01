import ast
import codegen
import transformers
import environment

from visitors import ConstantFinder, Declarer
from transformers import Renamer

def _(filename, output_file=None, original=False):
    return __(filename, output_file, original).compile()

class __(object):

    def __init__(self, filename, output_file, original):
        self.filename = filename
        self.output_file = output_file
        self.original = original
        self.code = open(filename).read()
        self.tree = ast.parse(self.code)
        self.env = environment.Environment(self.tree)

    def compile(self):
        constant_finder = ConstantFinder(self.env)
        declarer = Declarer(self.env)
        renamer = Renamer(self.env)

        for visitor in [constant_finder, declarer, renamer]:
            visitor.visit(self.tree)

        if constant_finder:
            assign_node = constant_finder.assignNode()
            self.tree.body = [assign_node] + self.tree.body 

        if renamer:
            assign_node = renamer.assignNode()
            self.tree.body = [assign_node] + self.tree.body 

        ret = codegen.to_source(self.tree)

        if self.output_file:
            with open(self.output_file, 'w') as out:
                if self.original:
                    for line in self.code.splitlines():
                        out.write('#  ' + line + '\n')
                    out.write('\n')
                out.write(ret)
        return ret

# Find out all constants

