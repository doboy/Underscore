import ast
import codegen

from variable_visitor import VariableVisitor
from constant_visitor import ConstantVisitor

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
        VariableVisitor(self.env).visit(self.tree)
        ConstantVisitor(self.env).visit(self.tree)
        output = codegen.to_source(self.tree)

        if self.output_file:
            self.writeout(output)

        return output

    def writeout(self, output):
        with open(self.output_file, 'w') as out:
            if self.original:
                self.writeoutOriginal(out)
                out.write('\n')
            out.write(output)

    def writeoutOriginal(self, out):
        for line in self.code.splitlines():
            out.write('#  ' + line + '\n')
