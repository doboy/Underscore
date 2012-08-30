#!/usr/bin/python

import nose.tools as nt
import glob
import underscore
import re

KEYWORDS = {'def', 'pass', 'print', 'global', 'if', 'class'}
BUILTINS = {'True', 'False', 'None'}
IDENTIFER_REGEX = '[a-zA-Z][a-zA-Z0-9]*'

def testGenerator():
    for filename in glob.glob('examples/*.py'):
        yield _testFile, filename

def _testFile(filename):
    underscored = underscore.compile(filename)
    for _id in re.findall(IDENTIFER_REGEX, underscored):
        nt.assert_in(_id, KEYWORDS | BUILTINS, 
                     'Id "{id}" did not get converted'.format(id=_id))
