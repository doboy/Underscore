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

TESTS_TO_SKIP_BY_VERSION = {
    (3, 3): set([
            'examples/assert.py',
            'examples/bases.py',
            'examples/basic_recursive.py',
            'examples/bool_op.py',
            'examples/call.py',
            'examples/chain_assignments.py',
            'examples/class_attribute.py',
            'examples/class_method.py',
            'examples/class_trivial.py',
            'examples/complex_import.py',
            'examples/complex_signature.py',
            'examples/comprehension.py',
            'examples/conditionally_existing_else.py',
            'examples/conditionally_existing_if_else.py',
            'examples/conditionally_existing_try.py',
            'examples/conditionally_existing_while_for.py',
            'examples/decorator.py',
            'examples/decorators.py',
            'examples/deep_imports2.py',
            'examples/del.py',
            'examples/del2.py',
            'examples/destructuring_assignment.py',
            'examples/doc_strings.py',
            'examples/empty_return_statement.py',
            'examples/finnally.py',
            'examples/for_while_else.py',
            'examples/function_arguments.py',
            'examples/global_defined_inside_function.py',
            'examples/global_function.py',
            'examples/if-else-statements.py',
            'examples/import_in_except2.py',
            'examples/lambda.py',
            'examples/nested_functions.py',
            'examples/raise.py',
            'examples/readme_example.py',
            'examples/scope_function.py',
            'examples/simple_function.py',
            'examples/slice.py',
            'examples/static_class_method.py',
            'examples/strings.py',
            'examples/subscription.py',
            'examples/trivial_function.py',
            'examples/trivial_import.py',
            'examples/try_example.py',
            'examples/yield.py'
            ])
}

def testGenerator():
    version = major, minor = sys.version_info[:2]
    tests_to_skip = TESTS_TO_SKIP_BY_VERSION.get(version, set())
    for filename in glob.glob('examples/*.py'):
        if filename in tests_to_skip:
            continue
        else:
            yield _testFile, filename

def _testFile(original_file):
    underscored_file = os.path.join('examples', 'underscored',
                               os.path.basename(original_file))
    _(original_file, underscored_file, original=True)
    nt.assert_equal(execute(original_file),
                    execute(underscored_file))
