"""Test to check if the example files are not empty."""

import glob
from underscore import _
from nose import tools as nt

def testEmpty():
    for filename in glob.glob('examples/*.py'):
        _testFile(filename)

def _testFile(filename):
    underscored = _(filename, write=False)
    nt.assert_not_equal(underscored.strip(), '', filename)

