import ast
import base

from also import also

class Renamer(base.BaseVisitor):

    def getNewName(self, old_name):
        assert isinstance(old_name, str), old_name
        new_name = self._current_frame.getId(old_name)
        return new_name or old_name
        
    def visit_Assign(self, node):
        for target in node.targets:
            self.generic_rename(target)
        ast.NodeVisitor.generic_visit(self, node.value)

    def visit_ClassDef(self, node):
        node.name = self.getNewName(node.name)
        with self.extendFrame(node):
            ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        node.name = self.getNewName(node.name)
        with self.extendFrame(node):
            self.generic_visit(node)

    @also('visit_Name')
    def visit_Global(self, node):
        self.generic_rename(node)

    def generic_rename(self, target):
        specific_rename = 'rename_' + type(target).__name__
        getattr(self, specific_rename)(target)

    def renames(self, names):
        for i, name in enumerate(names):
            names[i] = self.getNewName(name)
        print names

    def rename_Global(self, node):
        self.renames(node.names)

    def rename_Name(self, node):
        node.id = self.getNewName(node.id)

    def rename_Subscript(self, node):
        # TODO DELETE THIS
        ast.NodeVisitor.generic_visit(self, node)
    
    @also('rename_List')
    def rename_Tuple(self, node):
        for element in node.elts:
            self.generic_rename(element)
