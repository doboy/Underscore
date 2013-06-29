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
