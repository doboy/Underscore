import StringIO
import sys

FAILURES  = {}

class TestRun(object):
    def __init__(self, test, env=None):
        self.test = test
        self.env = env if env else {}

    def __enter__(self):
        self._codeOut = StringIO.StringIO()
        sys.stdout = self._codeOut
        return self

    def __exit__(self, _type, _value, _traceback):
        sys.stdout = sys.__stdout__
        self._codeOut.close()
        if _type:
            sys.stdout.write('F')
            FAILURES[self.test] = _type, _value, _traceback
        else:
            sys.stdout.write('.')
        return True

    def execute(self, filename):
        code = open(filename).read()
        exec code in self.env
        output = self._codeOut.getvalue()
        self._codeOut.truncate(0)
        return output
