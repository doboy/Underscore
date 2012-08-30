import glob
import re

from keyword import kwlist
from nose import tools as nt
from underscore import _

KEYWORDS = set(kwlist)
BUILT_INS = {'None', 'False', 'True', 'xrange', 'type'}
IDENTIFER_REGEX = '[a-zA-Z][a-zA-Z0-9]*'

def testGenerator():
    for filename in glob.glob('examples/*.py'):
        yield _testFile, filename

def _ids(code):
    for _id in re.findall(IDENTIFER_REGEX, code):
        yield _id

def _testFile(filename):
    error_msg = 'Id "{id}" on line {lineno} did not get converted'
    underscored = _(filename)
    for lineno, line in enumerate(underscored.splitlines()):
        if 'import' in line:
            continue
        for _id in _ids(line):
            nt.assert_in(_id, KEYWORDS | BUILT_INS, 
                         error_msg.format(id=_id, lineno=lineno))

