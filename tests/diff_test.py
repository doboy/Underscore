import glob
import os.path
import sys
import warnings

from nose import tools as nt
from underscore import _

try:
    import StringIO
except ImportError:
    from io import StringIO

def testGenerator():
    for filename in glob.glob('examples/*.py'):
        yield _testFile, filename

def _testFile(original_file):
    underscored_file = os.path.join('examples', 'underscored', 
                               os.path.basename(original_file))
    _(original_file, underscored_file, original=True)
    expected_output = _execute(original_file)
    actual_output = _execute(underscored_file)
    nt.assert_equal(actual_output, expected_output)

def _execute(filename):
    sys.stdout = fileOut = StringIO.StringIO()
    with open(filename) as python_file:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(python_file.read(), {})
    sys.stdout = sys.__stdout__
    output = fileOut.getvalue()
    fileOut.close()
    return output
