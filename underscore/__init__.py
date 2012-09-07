import ast
import glob
import os

from underscore import codegen
from underscore import variable_visitor
from underscore import constant_visitor

def _(src, dest=None, original=False, verbose=False):
    return __(src, dest, original, verbose).compile()

class __(object):

    def __init__(self, src, dest=None, original=False, verbose=True):
        self.src = src
        self.dest = dest
        __.original = original
        __.verbose = verbose

    def compile(self):
        self._genericCompile(self.src, self.dest)

    @staticmethod
    def _genericCompile(src, dest):
        if src == dest:
            raise ValueError('_: {src} and {dest} are the same location'.
                             format(src=src, dest=dest))
        while src.endswith('/'):
            src = src[:-1]
        head, tail = os.path.split(src)
        if dest is None:
            dest = os.path.join(head, '_' + tail)
        
        if os.path.isdir(src):
            return __._compileDir(src, dest)
        elif os.path.isfile(src):
            return __._compileFile(src, dest)
        else:
            raise ValueError('_: {src}: No such file or directory'.
                             format(src=src))

    @staticmethod
    def _compileFile(filename, dest):
        if os.path.isdir(dest):
            dest = os.path.join(dest, os.path.basename(filename))
            

        if __.verbose:
            print 'compiling {src} -> {dest}'.format(
                src=filename, dest=dest)

        original_code = open(filename).read()
        output = __._compileCode(original_code)
        __._writeout(output, dest, original_code)

    @staticmethod
    def _compileDir(dirname, destdir):
        if os.path.isfile(destdir):
            raise ValueError('_: {desination} is a file, expected directory'.
                             format(desination=destdir))

        if not os.path.isdir(destdir):
            os.mkdir(destdir)

        for item in os.listdir(dirname):
            src = os.path.join(dirname, item)
            if os.path.isdir(src) or src.endswith('.py'):
                dest = os.path.join(destdir, item)
                __._genericCompile(src, dest)

    @staticmethod
    def _compileCode(code):
        tree = ast.parse(code)
        __._underscoreTree(tree)
        return codegen.to_source(tree)
        
    @staticmethod
    def _underscoreTree(tree):
        env = environment.Environment(tree)
        variable_visitor.VariableVisitor(env).traverse()
        constant_visitor.ConstantVisitor(env).traverse()
        return tree

    @staticmethod
    def _writeout(output, dest, original_code):
        with open(dest, 'w') as out:
            if __.original: 
                __._writeoutOriginal(out, original_code)
            out.write(output)

    @staticmethod
    def _writeoutOriginal(out, original_code):
        for line in original_code.splitlines():
            out.write('#  ' + line + '\n')
        out.write('\n')
