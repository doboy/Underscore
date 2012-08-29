import ast, Environment

class Renamer(ast.NodeVisitor):
    def __init__(self):
        self._current_env = None

    def visit_Module(self, node):
        self._current_env = node.environment = Environment.THE_GLOBAL_ENVIRONMENT
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        self.generic_rename(node.targets)

    def visit_Name(self, node):
        self.rename_Name(node)

    def generic_rename(self, targets):
        for target in targets:
            specific_rename = 'rename_' + type(target).__name__
            getattr(self, specific_rename)(target)

    def rename_Name(self, node):
        _id = self._current_env.getId(node.id)
        # _id is None if we were unable to retrive the name
        if _id is not None:
            node.id = '_' * _id

    def rename_Subscript(self, node):
        # subscriptions do not bind declaration, so carry on..
        ast.NodeVisitor.generic_visit(self, node)
