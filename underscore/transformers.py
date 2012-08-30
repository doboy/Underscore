import ast
import base

from also import also

class Renamer(base.BaseVisitor):

    def getNewName(self, old_name):
        assert isinstance(old_name, str), old_name
        new_name = (self._current_frame.getNewName(old_name) or 
                    self.env.generateAndInjectNextDeclaration(old_name))
        return new_name
    
    def visit_Assign(self, node):
        for target in node.targets:
            self.generic_rename(target)
        ast.NodeVisitor.generic_visit(self, node.value)

    @also('visit_FunctionDef')
    def visit_ClassDef(self, node):
        node.name = self.getNewName(node.name)
        with self.Frame(node):
            self.generic_visit(node)

    def visit_Num(self, node):
        self.env.InjectConstant(node, node.n)

    def visit_Str(self, node):
        self.env.InjectConstant(node, node.s)

    @also('visit_ImportFrom')
    def visit_Import(self, node):
        for alias in node.names:
            assert alias.asname is not None
            alias.asname = self.getNewName(alias.asname)

    @also('visit_Name')
    def visit_Global(self, node):
        self.generic_rename(node)

    def generic_rename(self, target):
        specific_rename = 'rename_' + type(target).__name__
        getattr(self, specific_rename)(target)

    def rename_Global(self, node):
        for i, name in enumerate(node.names):
            node.names[i] = self.getNewName(name)

    def rename_Name(self, node):
        node.id = self.getNewName(node.id)

    def rename_Subscript(self, node):
        base.BaseVisitor.generic_visit(self, node)
    
    @also('rename_List')
    def rename_Tuple(self, node):
        for element in node.elts:
            self.generic_rename(element)


class Changer(ast.NodeTransformer):
    
    def __init__(self, env):
        self.env = env

    def visit_Num(self, node):
        if node.n in self.env._constants:
            return ast.copy_location(ast.Name(id=self.env._constants[node.n]), node)
        else:
            return node

    def visit_Str(self, node):
        return ast.copy_location(ast.Name(id=self.env._constants[node.s]), node)
