import ast

VALUE_FUNC = {ast.Num:  lambda node: node.n,
              ast.Str:  lambda node: node.s,
              ast.Name: lambda node: node.id}

class AssignmentManager(object):
    def __init__(self):
        self.aliases = {}
        self.assignments = {}

    def assign_node(self):
        target_elts = []
        value_elts = []
        for name, node in sorted(self.assignments.items()):
            target_elts.append(ast.Name(id=name, ctx=ast.Store()))
            value_elts.append(node)
        return ast.Assign(targets=[ast.Tuple(elts=target_elts)],
                          value=ast.Tuple(elts=value_elts))

    def add_assignment(self, left_name, right_node):
        val = valueOf(right_node)
        self.aliases[val] = left_name
        self.assignments[left_name] = right_node

    def get_new_name(self, old_name):
        return self.aliases.get(old_name)

class FrameContextManager(object):

    def __init__(self, frame, visitor):
        self.frame = frame
        self.visitor = visitor

    def __enter__(self):
        self.visitor._current_frame = self.frame
        return self.frame
    
    def __exit__(self, *_):
        self.visitor.withdraw_frame()

def valueOf(node):
    return VALUE_FUNC[type(node)](node)

