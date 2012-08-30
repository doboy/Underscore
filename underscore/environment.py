from collections import defaultdict

def generateId():
    count = 1
    while True:
        yield '_' * count
        count += 1

class Environment(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.declarations = defaultdict(generateId().next)

    def __contains__(self, name):
        return name in self.declarations

    def __getitem__(self, name):
        return self.declarations[name]

    def add(self, name):
        """Add a declaration into declarations, this can be down just 
        by accessing the element. If the element is not in the dict
        generateId will be called. If it is in it generateId wont be called.
        """
        self.declarations[name]

    def getId(self, name):
        """Returns an unique id, variables scoped differently will have 
        different ids even if they have the same name. Returns None if
        we cannot find the declaration of the name, meaning either built-in, 
        (from blah import *)ed or misstyped.
        """
        env = self._LookUpEnv(name)
        if env:
            return env[name]

    def _LookUpEnv(current_env, name):
        """Returns the environment that contains the defintion of name."""
        while current_env is not None:
            if name in current_env:
                return current_env
            else:
                current_env = current_env.parent
    
# Alias Frame and Environment
Frame = Environment
