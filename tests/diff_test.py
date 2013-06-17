import glob
import os
import sys

from nose import tools as nt
from underscore import _
from test_utils import execute

def testGenerator():
    major, minor = sys.version_info[:2]
    version_tests = glob.glob('examples/*.py' + str(major) + '.' + str(minor))
    for filename in glob.glob('examples/*.py') + version_tests:
        yield _testFile, filename

def _testFile(original_file):
    underscored_file = os.path.join('examples', 'underscored',
                               os.path.basename(original_file))
    _(original_file, underscored_file, original=True)
    nt.assert_equal(execute(original_file),
                    execute(underscored_file))

