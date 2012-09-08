class Declaration(object):
    def __init__(self, name):
        self.name = name
        self.global_ = False
        self.delete = False
        self._conditional = None

    @property
    def conditional(self):
        assert self._conditional is not None
        return self.delete or self._conditional

def generator():
    _ = '_'
    while True:
        # yield Declaration('_' + str(len(_)))
        yield Declaration(_)
        _ += '_'
