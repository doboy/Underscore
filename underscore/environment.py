import ast
from collections import defaultdict

class Declaration(object):
    def __init__(self, name):
        self.name = name
        self.global_ = False
    
    @staticmethod
    def generateDeclaration():
        _ = '_'
        while True:
            yield Declaration(_)
            _ += '_'

class Environment(object):
    def __init__(self, tree):
        self.generator = Declaration.generateDeclaration()
        self._global_frame = Frame(env=self)
        self._tree = tree
        self._constants = {}
        self._constants_assign_node = None
        self._initial_assign_node = None

    def generateNextDeclaration(self):
        return self.generator.next()

    def generateAndInjectNextDeclaration(self, old_name):
        self._global_frame.add(old_name, global_=True)
        new_name = self._global_frame[old_name].name

        if self._initial_assign_node is None:
            self._initial_assign_node = self.createInitialAssignNode()
        
        self._injectAssignment(self._initial_assign_node, new_name, old_name)
        return new_name

    def InjectConstant(self, node, constant):
        if constant not in self._constants:
            if self._constants_assign_node is None:
                self._constants_assign_node = self.createInitialConstantNode()
            declaration = self.generateNextDeclaration()
            self._constants[constant] = declaration.name
            self._injectAssignment(self._constants_assign_node, declaration.name, str(constant))

    def _injectAssignment(self, node, left_name, right_name):
        node.targets[0].elts.append(ast.Name(id=left_name, ctx=ast.Store()))
        node.value.elts.append(ast.Name(id=right_name, ctx=ast.Load()))

    def _injectConstantAssignment(self, node, left_name, constant):
        node.targets[0].elts.append(ast.Name(id=left_name, ctx=ast.Store()))
        node.value.elts.append(constant)

    def createInitialAssignNode(self):
        node = ast.Assign(targets=[ast.Tuple(elts=[])], value=ast.Tuple(elts=[]))
        self._tree.body = [node] + self._tree.body
        return node

    def createInitialConstantNode(self):
        node = ast.Assign(targets=[ast.Tuple(elts=[])], value=ast.Tuple(elts=[]))
        self._tree.body = [node] + self._tree.body
        return node

class Frame(object):
    def __init__(self, parent=None, env=None):
        if parent is not None:
            self.parent = parent
            self.env = parent.env
        elif env is not None:
            self.parent = None
            self.env = env
        else:
            raise ValueError('Invalid argument combintation')
        self.declarations = defaultdict(self.env.generateNextDeclaration)

    def __contains__(self, name):
        return name in self.declarations

    def __getitem__(self, name):
        return self.declarations[name]

    def add(self, name, global_=False):
        """Add a declaration into declarations, this can be down just 
        by accessing the element. If the element is not in the dict
        generateId will be called. If it is in it generateId wont be called.
        """
        self.declarations[name].global_ |= global_

    def getNewName(self, name):
        """Returns an unique id, variables scoped differently will have 
        different ids even if they have the same name. Returns None if
        we cannot find the declaration of the name, meaning either built-in, 
        (from blah import *)ed or misstyped.
        """
        try:
            frame = self._LookUpEnv(name)
            declaration = frame[name]
            if declaration.global_:
                declaration = frame.env._global_frame[name]
            return declaration.name
        except TypeError as e:
            pass

    def _LookUpEnv(current_env, name):
        """Returns the environment that contains the defintion of name."""
        while current_env is not None:
            if name in current_env:
                return current_env
            else:
                current_env = current_env.parent
