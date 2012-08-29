import ast, environment

class Renamer(ast.NodeVisitor):
    def __init__(self, current_frame=None):
        if current_frame is None:
            current_frame = environment.Frame()
        self._global_frame = self._current_frame = current_frame

    def withdrawFrame(self):
        self._current_frame = self._current_frame.parent

    def visit_Assign(self, node):
        self.generic_renames(node.targets)

    def visit_FunctionDef(self, node):
        _id = self._current_frame.getId(node.name)
        if _id is not None:
            node.name = '_' * _id
        self._current_frame = node.frame
        ast.NodeVisitor.generic_visit(self, node)
        self._current_frame = node.frame.parent

    def visit_Name(self, node):
        self.rename_Name(node)

    def visit_Global(self, node):
        self.generic_rename(node)

    def generic_renames(self, targets):
        for target in targets:
            self.generic_rename(target)

    def generic_rename(self, target):
        specific_rename = 'rename_' + type(target).__name__
        getattr(self, specific_rename)(target)

    def rename_Global(self, node):
        for idx in xrange(len(node.names)):
            name = node.names[idx]
            _id = self._global_frame.getId(name)
            if _id is not None:
                node.names[idx] = '_' * _id 

    def rename_Name(self, node):
        _id = self._current_frame.getId(node.id)
        # _id is None if we were unable to retrive the name
        if _id is not None:
            node.id = '_' * _id

    def rename_Subscript(self, node):
        # subscriptions do not bind declaration, so carry on..
        ast.NodeVisitor.generic_visit(self, node)

    def rename_Tuple(self, node):
        for element in node.elts:
            self.generic_rename(element)

    rename_List = rename_Tuple
