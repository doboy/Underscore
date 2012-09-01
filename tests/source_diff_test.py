import glob
import os.path
import sys
import StringIO
import warnings

from nose import tools as nt
from underscore import _

def testGenerator():
    for filename in glob.glob('underscore/*.py'):
        yield _testFile, filename

def _testFile(original_file):
    underscored_file = os.path.join('underscore', 'underscored', 
                               os.path.basename(original_file))
    _(original_file, underscored_file, True)
    expected_output = _execute(original_file)
    actual_output = _execute(underscored_file)
    nt.assert_equal(actual_output, expected_output)

def _execute(filename):
    sys.stdout = fileOut = StringIO.StringIO()
    with open(filename) as python_file:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec python_file.read() in {}
    sys.stdout = sys.__stdout__
    output = fileOut.getvalue()
    fileOut.close()
    return output
