import ast
import Environment

class Declarer(ast.NodeVisitor):
    def __init__(self):
        self._current_env = None

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        
    def visit_Module(self, node):
        self._current_env = node.environment = Environment.THE_GLOBAL_ENVIRONMENT
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        self.generic_declare(node.targets)

    def generic_declare(self, targets):
        for target in targets:
            specific_declare = 'declare_' + type(target).__name__
            getattr(self, specific_declare)(target)

    def declare_Name(self, node):
        self._current_env.add(node.id)

    def declare_Subscript(self, node):
        # subscriptions do not bind declaration, so carry on..
        ast.NodeVisitor.generic_visit(self, node)
