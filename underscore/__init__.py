#!/usr/bin/python

import ast
import codegen
import sys
import transformers
import visitors

def Underscore(code):
    tree = ast.parse(code)
    visitor = visitors.Declarer()
    visitor.visit(tree)
    
    renamer = transformers.Renamer()
    renamer.visit(tree)
    
    return codegen.to_source(tree)


def Usage():
    usage = """
Usage: underscore [file]
"""
    print >>sys.stderr, usage
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        Usage()
    else:
        print Underscore(open(sys.argv[1]).read())
