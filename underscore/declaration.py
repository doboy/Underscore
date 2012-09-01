class Declaration(object):
    def __init__(self, name):
        self.name = name
        self.global_ = False
    
    def __hash__(self):
        return len(self.name) * 2 + self.global_

    def __eq__(self, other):
        return self.global_ == other.global_ and \
            self.name == other.name

def generator():
    _ = '_'
    while True:
        # yield Declaration('_' + str(len(_)))
        yield Declaration(_)
        _ += '_'
