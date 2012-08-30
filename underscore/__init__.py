import ast
import codegen
import transformers
import visitors
import environment

def _(filename, output_file=None, original=False):
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
