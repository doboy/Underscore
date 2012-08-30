import ast
import base

from also import also

class Declarer(base.BaseVisitor):

    def visit_Assign(self, node):
        for target in node.targets:
            self.generic_declare(target)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):
        self.declare(node.name)
        with self.extendFrame(node):
            ast.NodeVisitor.generic_visit(self, node)

    def visit_For(self, node):
        self.generic_declare(node.target)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        self.declare(node.name)
        with self.extendFrame(node):
            for arg in node.args.args:
                self.generic_declare(arg)
            ast.NodeVisitor.generic_visit(self, node)

    def visit_Global(self, node):
        for name in node.names:
            self.declare(name)

    def generic_declare(self, target):
        specific_declare = 'declare_' + type(target).__name__
        getattr(self, specific_declare)(target)

    def declare(self, name, frame=None):
        assert isinstance(name, str), name
        frame = frame or self._current_frame
        frame.add(name)

    def declare_Global(self, node):
        for name in node.names:
            self.declare(name, frame=self._global_frame)
        
    def declare_Name(self, node):
        self.declare(node.id)

    def declare_Subscript(self, node):
        # TODO DELETE THIS
        ast.NodeVisitor.generic_visit(self, node)

    @also('declare_List')
    def declare_Tuple(self, node):
        for element in node.elts:
            self.generic_declare(element)

    def declare_arguments(self, node):
        for name in node.args:
            self._current_frame.add(name)
