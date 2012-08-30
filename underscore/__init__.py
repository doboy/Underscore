import ast
import codegen
import transformers
import visitors
import environment

def _(filename, output_file=None, original=False):
    code = open(filename).read()

    env = environment.Environment()

    tree = ast.parse(code)

    visitor = visitors.Declarer(env)
    visitor.visit(tree)
    
    renamer = transformers.Renamer(env)
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
