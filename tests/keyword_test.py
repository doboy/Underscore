import ast
import glob

from underscore import _
from underscore import environment
from underscore import utils
from underscore import variable_visitor
from nose import tools as nt

class KeywordVisitor( variable_visitor._VariableFinder):
    def declare(self, name, _global=False):
        if name != '_' * len(name):
            nt.assert_not_in(name, self._current_frame)
            self._current_frame.add(name, _global)

def testGenerator():
    for filename in glob.glob('examples/*.py'):
        yield _testFile, filename

def _testFile(filename):
    underscored = _(filename, write=False)
    tree = ast.parse(underscored)
    env = environment.Environment(tree)
    visitor = KeywordVisitor(env, utils.AssignmentManager())
    visitor.visit(tree)
