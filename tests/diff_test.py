import glob
import os.path
import sys
import warnings

from nose import tools as nt
from underscore import _
from StringIO import StringIO

def testGenerator():
    ver = sys.version_info
    if ver >= (2, 7):
        version_tests = glob.glob('examples/*.py' + str(ver.major) + '.' + str(ver.minor))
    else:
        version_tests = str(ver[0]) + '.' + str(ver[1])
    for filename in glob.glob('examples/*.py') + version_tests:
        yield _testFile, filename

def _testFile(original_file):
    underscored_file = os.path.join('examples', 'underscored', 
                               os.path.basename(original_file))
    _(original_file, underscored_file, original=True)
    expected_output = _execute(original_file)
    actual_output = _execute(underscored_file)
    nt.assert_equal(actual_output, expected_output)

def _execute(filename):
    sys.stdout = fileOut = StringIO()
    with open(filename) as python_file:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(python_file.read(), {})
    sys.stdout = sys.__stdout__
    output = fileOut.getvalue()
    fileOut.close()
    return output
