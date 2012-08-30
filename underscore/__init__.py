import ast
import codegen
import transformers
import visitors
import environment

def _(filename, output_file=None, original=False):
    code = open(filename).read()
    tree = ast.parse(code)
    env = environment.Environment(tree)
    declarer = visitors.Declarer(env)
    renamer = transformers.Renamer(env)
    changer = transformers.Changer(env)
    declarer.visit(tree)
    renamer.visit(tree)
    changer.visit(tree)
    ret = codegen.to_source(tree)
    if output_file:
        with open(output_file, 'w') as out:
            if original:
                for line in code.splitlines():
                    out.write('#  ' + line + '\n')
                out.write('\n')
            out.write(ret)
            
    return ret
