#!/usr/bin/python

import ast
import codegen
import sys
import transformers
import visitors
import environment

def compile(filename, output_file=None, original=False):
    code = open(filename).read()

    global_frame = environment.Frame()

    tree = ast.parse(code)

    visitor = visitors.Declarer(global_frame)
    visitor.visit(tree)
    
    renamer = transformers.Renamer(global_frame)
    renamer.visit(tree)
    
    ret = codegen.to_source(tree)
    if output_file:
        with open(output_file, 'w') as out:
            if original:
                for line in code.splitlines():
                    out.write('#  ' + line + '\n')
                out.write('\n')
            out.write(ret)
            
    return ret

def usage():
    print >>sys.stderr, (
        "\n"
        "Usage: underscore [file]"
        "\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    else:
        print compile(sys.argv[1])

__all__ = ['compile']
