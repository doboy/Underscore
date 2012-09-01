import ast

class AssignmentManager(object):
    def __init__(self):
        self.assignments = {}

    def __nonzero__(self):
        return bool(self.assignments)

    def assignNode(self):
        target_elts = []
        value_elts = []
        for name, node in sorted(self.assignments.items()):
            target_elts.append(ast.Name(id=name, ctx=ast.Store()))
            value_elts.append(node)
        return ast.Assign(targets=[ast.Tuple(elts=target_elts)],
                          value=ast.Tuple(elts=value_elts))

    def addAssignment(self, left_name, right_node):
        self.assignments[left_name] = right_node


class FrameContextManager(object):

    def __init__(self, frame, visitor):
        self.frame = frame
        self.visitor = visitor

    def __enter__(self):
        self.visitor._current_frame = self.frame
        return self.frame
    
    def __exit__(self, *_):
        self.visitor.withdrawFrame()
