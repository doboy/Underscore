import ast
import base

from also import also

class Renamer(base.BaseVisitor):

    def __init__(self, env):
        base.BaseVisitor.__init__(self, env)
        self._assignmentManager = base.AssignmentManager()

    def assignNode(self):
        return self._assignmentManager

    def getNewName(self, old_name):
        assert isinstance(old_name, str), old_name
        new_name = self._current_frame.getNewName(old_name)
        if new_name is None:
            new_name = self.env.generateNextDeclaration().name
            self._assignmentManager.addAssignment(
                new_name, ast.Name(id=old_name, ctx=ast.Store()))
            return new_name
        else:
            return new_name
    
    def visit_Assign(self, node):
        for target in node.targets:
            self.generic_rename(target)
        self.visit(node.value)

    @also('visit_FunctionDef')
    def visit_ClassDef(self, node):
        node.name = self.getNewName(node.name)
        with self.Frame(node):
            self.generic_visit(node)

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

