import glob
import os

from nose import tools as nt
from underscore import _
from utils import execute

def testGenerator():
    try: os.mkdir('tests/tmp')
    except: pass
        
    for filename in glob.glob('src/*.py'):
        yield _testFile, filename

def _testFile(original_file):
    underscored_file = os.path.join('tests', 'tmp',
                                    os.path.basename(original_file))
    _(original_file, underscored_file, original=True)
    nt.assert_equal(execute(original_file),
                    execute(underscored_file))
