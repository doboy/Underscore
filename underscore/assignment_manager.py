import ast

from utils import value_of, \
    VALUE_FUNC

class AssignmentManager(object):
    def __init__(self):
        self.aliases = {}
        self.assignments = {}

    def get_assign_node(self):
        target_elts = []
        value_elts = []
        for name, node in sorted(self.assignments.items()):
            target_elts.append(ast.Name(id=name, ctx=ast.Store()))
            value_elts.append(node)
        return ast.Assign(targets=[ast.Tuple(elts=target_elts)],
                          value=ast.Tuple(elts=value_elts))

    def add_assignment(self, left_name, right_node):
        val = value_of(right_node)
        self.aliases[val] = left_name
        self.assignments[left_name] = right_node

    def get_new_name(self, old_name):
        return self.aliases.get(old_name)
