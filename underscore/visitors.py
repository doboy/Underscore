import ast
import environment

class Declarer(ast.NodeVisitor):
    def __init__(self, current_frame=None):
        if current_frame is None:
            current_frame = environment.Frame()
        self._global_frame = self._current_frame = current_frame

    def extendFrame(self, node):
        node.frame = self._current_frame = environment.Frame(
            self._current_frame)

    def withdrawFrame(self):
        self._current_frame = self._current_frame.parent

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        self.generic_declares(node.targets)

    def visit_FunctionDef(self, node):
        # Functions declares a new scope, so create a frame
        self._current_frame.add(node.name)
        self.extendFrame(node)
        self.generic_declare(node.args)
        ast.NodeVisitor.generic_visit(self, node)
        self.withdrawFrame()

    def visit_Global(self, node):
        self.generic_declare(node)

    def generic_declares(self, targets):
        for target in targets:
            self.generic_declare(target)

    def generic_declare(self, target):
        specific_declare = 'declare_' + type(target).__name__
        getattr(self, specific_declare)(target)

    def declare_Global(self, node):
        for name in node.names:
            self._global_frame.add(name)
        
    def declare_Name(self, node):
        self._current_frame.add(node.id)

    def declare_Subscript(self, node):
        # subscriptions do not bind declaration, so carry on..
        ast.NodeVisitor.generic_visit(self, node)

    def declare_Tuple(self, node):
        for element in node.elts:
            self.generic_declare(element)

    def declare_arguments(self, node):
        # TODO
        pass
    
    declare_List = declare_Tuple
