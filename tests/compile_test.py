import os
import shutil
import unittest
from underscore import _

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def tmp(*filename):
    return os.path.join('tests/tmp', *filename)

class BaseCompileTest(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree(tmp())
        except:
            pass
        os.mkdir(tmp())

    def tearDown(self):
            shutil.rmtree(tmp())

    def clean(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            # no file exists
            pass

    def touch(self, filename):
        self.clean(filename)
        touch(filename)

    def mkdir(self, dirname):
        self.clean(dirname)
        os.mkdir(dirname)
    
    # Python 2.6 compat
    class contextManager(object):
        def __init__(self, exception_type):
            self.exception_type = exception_type

        def __enter__(self):
            return self

        def __exit__(self, _type, value, traceback):
            self.exception = value
            return isinstance(value, self.exception_type)

    def assertRaises(self, exception):
        return self.contextManager(exception)
    # Python 2.6 compat


class SadPathCompileTest(BaseCompileTest):
    """Testing the compile function."""

    def testNonExistingSource(self):
        self.clean(tmp('bar'))
        with self.assertRaises(ValueError) as e:
            _(tmp('bar'))
        self.assertEquals(str(e.exception), 
                          '_: %s: No such file or directory' % tmp('bar'))

    def testSourceSameAsDest(self):
        self.touch(tmp('car'))
        with self.assertRaises(ValueError) as e:
            _(tmp('car'), tmp('car'))
        self.assertEquals(str(e.exception), 
                          '_: %s and %s are the same' % (
                tmp('car'), tmp('car')))

        with self.assertRaises(ValueError) as e:
            _(tmp('far'), tmp('far'))
        self.assertEquals(str(e.exception), 
                          '_: %s and %s are the same' % (
                tmp('far'), tmp('far')))

    def testSourceDirDestFile(self):
        self.touch(tmp('foo.py'))
        self.mkdir(tmp('zar'))
        assert os.path.isdir(tmp('zar'))
        with self.assertRaises(ValueError) as e:
            _(tmp('zar'), tmp('foo.py'))
        self.assertEquals(str(e.exception), 
                          '_: %s is a file, expected directory' % tmp('foo.py'))
        
class HappyPathCompileTest(BaseCompileTest):
    def testSimpleFileCompile(self):
        self.touch(tmp('nar.py'))
        _(tmp('nar.py'))
        self.assertTrue(os.path.isfile(tmp('_nar.py')))

    def testSimpleFileCompile2(self):
        self.touch(tmp('dar.py'))
        _(tmp('dar.py'), tmp('ddar.py'))
        self.assertTrue(os.path.isfile(tmp('ddar.py')))
        self.assertFalse(os.path.isfile(tmp('_dar.py')))

    def testSimpleDirCompile(self):
        self.mkdir(tmp('gar'))
        _(tmp('gar'))
        self.assertTrue(os.path.isdir(tmp('_gar')))

    def testSimpleDirCompile2(self):
        self.mkdir(tmp('qar'))
        _(tmp('qar'), tmp('qqar'))
        self.assertTrue(os.path.isdir(tmp('qqar')))
        self.assertFalse(os.path.isdir(tmp('_qar')))
