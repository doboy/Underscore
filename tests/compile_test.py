"""
Tests the functionality of the '_'.
"""
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

    def touch(self, filename):
        touch(filename)

    def mkdir(self, dirname):
        os.mkdir(dirname)

    def _(self, *args):
        _(*args)

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
        with self.assertRaises(ValueError) as e:
            self._(tmp('bar'))
        self.assertEquals(str(e.exception),
                          '_: %s: No such file or directory' % tmp('bar'))

    def testSourceSameAsDest(self):
        self.touch(tmp('car'))
        with self.assertRaises(ValueError) as e:
            self._(tmp('car'), tmp('car'))
        self.assertEquals(str(e.exception),
                          '_: %s and %s are the same location' % (
                tmp('car'), tmp('car')))

        self.mkdir(tmp('far'))
        with self.assertRaises(ValueError) as e:
            self._(tmp('far'), tmp('far'))
        self.assertEquals(str(e.exception),
                          '_: %s and %s are the same location' % (
                tmp('far'), tmp('far')))

    def testSourceDirDestFile(self):
        self.touch(tmp('foo.py'))
        self.mkdir(tmp('zar'))
        assert os.path.isdir(tmp('zar'))
        with self.assertRaises(ValueError) as e:
            self._(tmp('zar'), tmp('foo.py'))
        self.assertEquals(str(e.exception),
                          '_: %s is a file, expected directory' % tmp('foo.py'))

class HappyPathCompileTest(BaseCompileTest):
    def testSimpleFileCompile(self):
        self.touch(tmp('nar.py'))
        self._(tmp('nar.py'))
        self.assertTrue(os.path.isfile(tmp('_nar.py')))

    def testSimpleFileCompile2(self):
        self.touch(tmp('dar.py'))
        self._(tmp('dar.py'), tmp('ddar.py'))
        self.assertTrue(os.path.isfile(tmp('ddar.py')))
        self.assertFalse(os.path.isfile(tmp('_dar.py')))

    def testFileToDirectoryCompile(self):
        self.touch(tmp('kar.py'))
        self.mkdir(tmp('lar'))
        self._(tmp('kar.py'), tmp('lar'))
        self.assertTrue(os.path.isfile(tmp('lar/kar.py')))

    def testSimpleDirCompile(self):
        self.mkdir(tmp('gar'))
        self._(tmp('gar'))
        self.assertTrue(os.path.isdir(tmp('_gar')))

    def testSimpleDirCompile2(self):
        self.mkdir(tmp('qar'))
        self._(tmp('qar'), tmp('qqar'))
        self.assertTrue(os.path.isdir(tmp('qqar')))
        self.assertFalse(os.path.isdir(tmp('_qar')))

    def testNonTrivialDirCompile(self):
        self.mkdir(tmp('sar'))
        self.mkdir(tmp('sar/far'))
        self.touch(tmp('sar/car.py'))
        self.touch(tmp('sar/far/war.py'))
        self._(tmp('sar'))
        self.assertTrue(os.path.isdir(tmp('_sar')))
        self.assertTrue(os.path.isdir(tmp('_sar/far')))
        self.assertTrue(os.path.isfile(tmp('_sar/car.py')))
        self.assertTrue(os.path.isfile(tmp('_sar/far/war.py')))

    def testNonTrivialDirCompile2(self):
        self.mkdir(tmp('jar'))
        self.mkdir(tmp('jar/far'))
        self.touch(tmp('jar/car.py'))
        self.touch(tmp('jar/far/war.py'))
        self._(tmp('jar'), tmp('nar'))
        self.assertTrue(os.path.isdir(tmp('nar')))
        self.assertTrue(os.path.isdir(tmp('nar/far')))
        self.assertTrue(os.path.isfile(tmp('nar/car.py')))
        self.assertTrue(os.path.isfile(tmp('nar/far/war.py')))
