class Declaration(object):
    def __init__(self, name):
        self.name = name
        self.global_ = False

def generator():
    _ = '_'
    while True:
        # yield Declaration('_' + str(len(_)))
        yield Declaration(_)
        _ += '_'
