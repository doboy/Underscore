import ast
import os

from underscore import codegen
from underscore import variable_visitor
from underscore import constant_visitor

def _(filename, output_file=None, original=False, write=True):
    return __(filename, output_file, original, write).compile()

class __(object):

    def __init__(self, source, destination=None, original=False, write=True):
        self.source = source
        self.destination = destination
        self.original = original
        self.write = write

    def compile(self):
        self._genericCompile(self.source, self.destination)

    def _genericCompile(self, source, destination):
        if os.path.isfile(source):
            return self._compileFile(source, destination)
        elif os.path.isdir(source):
            return self._compileDir(source, destination)
        else:
            raise ValueError('_: {source}: No such file or directory'.
                             format(source=self.source))

    def _compileFile(self, filename, destination):
        if filename == destination:
            raise ValueError('_: {source} and {destination} are the same file'.
                             format(source=filename, destination=destination))
        head, tail = os.path.split(filename)
        if destination is None:
            destination = os.path.join(head, '_' + tail)
        elif os.path.isdir(destination):
            os.path.join(head, tail, '_' + tail)
            
        original_code = open(filename).read()
        tree = ast.parse(original_code)

        self._underscoreTree(tree)
        output = codegen.to_source(tree)

        if self.write:
            self._writeout(output, destination, original_code)

        return output

    def _compileDir(self, dirname, destdir):
        if dirname == destdir:
            raise ValueError('_: {source} and {destination} are the same directory'.
                             format(source=dirname, destination=destdir))
        head, tail = os.path.split(dirname)
        if destdir is None:
            destdir = os.path.join(head, '_' + tail)
        elif os.path.isfile(destdir):
            raise ValueError('_: {desination} is a file, expected directory'.
                             format(desination=destdir))

        if not os.path.isdir(destdir):
            os.mkdir(destdir)

        for blob in os.listdir(dirname):
            self._genericCompile(os.path.join(dirname, blob),
                                 os.path.join(destdir, blob))
        
    def _underscoreTree(self, tree):
        env = environment.Environment(tree)
        variable_visitor.VariableVisitor(env).traverse()
        constant_visitor.ConstantVisitor(env).traverse()
        return tree

    def _writeout(self, output, destination, original_code):
        with open(destination, 'w') as out:
            if self.original: 
                self._writeoutOriginal(out, original_code)
            out.write(output)

    def _writeoutOriginal(self, out, original_code):
        for line in original_code.splitlines():
            out.write('#  ' + line + '\n')
        out.write('\n')
