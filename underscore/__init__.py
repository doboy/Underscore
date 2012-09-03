import ast
import codegen
import os

from variable_visitor import VariableVisitor
from constant_visitor import ConstantVisitor

def _(filename, output_file=None, original=False, write=True):
    return __(filename, output_file, original, write).compile()

class __(object):

    def __init__(self, source, destination=None, original=False, write=True):
        if source == destination:
            raise ValueError('_: {source} and {destination} are the same file'.format(
                    source=source, destination=destination))
        self.source = source
        self.destination = destination
        self.original = original
        self.write = write

    def compile(self):
        if os.path.isfile(self.source):
            return self.compileFile(self.source, self.destination)
        elif os.path.isdir(self.source):
            return self.compileDir(self.source, self.destination)
        else:
            raise ValueError('_: {source}: No such file or directory'.
                             format(source=self.source))

    def compileFile(self, filename, destination):
        head, tail = os.path.split(filename)
        if destination is None:
            destination = os.path.join(head, '_' + tail)
        elif os.path.isdir(destination):
            os.path.join(head, tail, '_' + tail)
        else:
            pass
            
        original_code = open(filename).read()
        tree = ast.parse(original_code)

        self.underscoreTree(tree)
        output = codegen.to_source(tree)

        if self.write:
            self.writeout(output, destination, original_code)

        return output

    def compileDir(self, dirname, destdir):
        head, tail = os.path.split(dirname)
        if destdir is None:
            destdir = os.path.join(head, '_' + tail)
        elif os.path.isfile(destdir):
            raise ValueError('_: {desination} is a file, expected directory'.
                             format(desination=destdir))
        elif not os.path.isdir(destdir):
            os.mkdir(destdir)

        for directory, _, filenames in os.walk(dirname):
            for filename in filenames:
                if filename.endswith('.py'):
                    source = os.path.join(dirname, filename)
                    destination = os.path.join(destdir, filename)
                    self.compileFile(source, destination)
        
    def underscoreTree(self, tree):
        env = environment.Environment(tree)
        VariableVisitor(env).visit(tree)
        ConstantVisitor(env).visit(tree)
        return tree
        
    def writeout(self, output, destination, original_code):
        with open(destination, 'w') as out:
            if self.original: 
                self.writeoutOriginal(out, original_code)
            out.write(output)

    def writeoutOriginal(self, out, original_code):
        for line in original_code.splitlines():
            out.write('#  ' + line + '\n')
        out.write('\n')
            
