import glob
import re

from nose import tools as nt
from underscore import _

KEYWORDS = {'def', 'pass', 'print', 'global', 
            'if', 'class', 'for', 'in', 'return'}
BUILT_INS = {'None', 'False', 'True', 'xrange'}
IDENTIFER_REGEX = '[a-zA-Z][a-zA-Z0-9]*'

def testGenerator():
    for filename in glob.glob('examples/*.py'):
        yield _testFile, filename

def _testFile(filename):
    underscored = _(filename)
    for _id in re.findall(IDENTIFER_REGEX, underscored):
        nt.assert_in(_id, KEYWORDS | BUILT_INS,
                     'Id "{id}" did not get converted'.format(id=_id))
