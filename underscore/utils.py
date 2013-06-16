import ast

VALUE_FUNC = {ast.Num:  lambda node: node.n,
              ast.Str:  lambda node: node.s,
              ast.Name: lambda node: node.id}

def value_of(node):
    return VALUE_FUNC[type(node)](node)
