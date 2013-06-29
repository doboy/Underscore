"""
For each python file in the examples directory, verifies that the output
of the original file matches the output of that file after going through
the underscore compiler.
"""
import glob
import os
import sys

from nose import tools as nt
from underscore import _
from test_utils import execute

def testGenerator():
    for filename in glob.glob('examples/*.py'):
        yield _testFile, filename

def _testFile(original_file):
    underscored_file = os.path.join('examples', 'underscored',
                               os.path.basename(original_file))
    _(original_file, underscored_file, original=True)
    nt.assert_equal(execute(original_file),
                    execute(underscored_file))
