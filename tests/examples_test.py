"""
For each python file in the examples directory, verifies that the output
of the original file matches the output of that file after going through
the underscore compiler.
"""
import ast
import glob
import os
import sys

from nose import tools as nt
from underscore import _
from test_utils import execute

TESTS_TO_SKIP_BY_VERSION = {
    (3, 3): set([
            'examples/complex_signature.py',
            'examples/comprehension.py',
            'examples/try_example.py',
            ])
}

def testGenerator():
    version = major, minor = sys.version_info[:2]
    tests_to_skip = TESTS_TO_SKIP_BY_VERSION.get(version, set())
    for filename in glob.glob('examples/*.py'):
        if filename in tests_to_skip:
            yield _testFailFile, filename
        else:
            yield _testFile, filename

def dump_ast(filename):
    with open(filename, "r") as fh:
        return ast.dump(
            ast.parse(fh.read()),
            annotate_fields=True,
            include_attributes=True)

def _testFile(original_filename):
    underscored_filename = os.path.join('examples', 'underscored',
                               os.path.basename(original_filename))
    _(original_filename, underscored_filename, original=True)

    try:
        original_filename_output = execute(original_filename)
    except:
        raise Exception(str(dump_ast(original_filename)))

    try:
        underscored_filename_output = execute(underscored_filename)
    except:
        exc_type, value = sys.exc_info()[:2]
        raise Exception(
            str(dump_ast(original_filename)) + '\n\n' +
            open(underscored_filename).read())

    nt.assert_equal(original_filename_output, underscored_filename_output)

def _testFailFile(original_filename):
    nt.assert_raises(Exception, _testFile, original_filename)
