import ast

class AssignmentManager(object):
    
    def __init__(self):
        self.node = ast.Assign(targets=[ast.Tuple(elts=[])], value=ast.Tuple(elts=[]))

    def __len__(self):
        return len(self.node.elts)

    def addAssignment(self, left_name, right_node):
        self.node.targets[0].elts.append(ast.Name(id=left_name, ctx=ast.Store()))
        self.node.value.elts.append(right_node)
