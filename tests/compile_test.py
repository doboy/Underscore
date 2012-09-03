import os
import shutil
import unittest
from underscore import _

def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)


class BaseCompileTest(unittest.TestCase):
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
    

class SadPathCompileTest(BaseCompileTest):
    """Testing the compile function."""

    def testNonExistingSource(self):
        self.clean('/tmp/bar')
        with self.assertRaises(ValueError) as e:
            _('/tmp/bar')
        self.assertEquals(str(e.exception), 
                          '_: /tmp/bar: No such file or directory')

    def testSourceSameAsDest(self):
        self.touch('/tmp/car')
        with self.assertRaises(ValueError) as e:
            _('/tmp/car', '/tmp/car')
        self.assertEquals(str(e.exception), 
                          '_: /tmp/car and /tmp/car are the same file')

        self.mkdir('/tmp/far')
        with self.assertRaises(ValueError) as e:
            _('/tmp/far', '/tmp/far')
        self.assertEquals(str(e.exception), 
                          '_: /tmp/far and /tmp/far are the same file')

    def testSourceDirDestFile(self):
        self.touch('/tmp/foo.py')
        self.mkdir('/tmp/zar')
        assert os.path.isdir('/tmp/zar')
        with self.assertRaises(ValueError) as e:
            _('/tmp/zar', '/tmp/foo.py')
        self.assertEquals(str(e.exception), 
                          '_: /tmp/foo.py is a file, expected directory')
        
class HappyPathCompileTest(BaseCompileTest):
    def testSimpleFileCompile(self):
        self.touch('/tmp/nar.py')
        _('/tmp/nar.py')
        self.assertTrue(os.path.isfile('/tmp/_nar.py'))

    def testSimpleFileCompile2(self):
        self.touch('/tmp/dar.py')
        _('/tmp/dar.py', '/tmp/ddar.py')
        self.assertTrue(os.path.isfile('/tmp/ddar.py'))
        self.assertFalse(os.path.isfile('/tmp/_dar.py'))

    def testSimpleDirCompile(self):
        self.mkdir('/tmp/gar')
        _('/tmp/gar')
        self.assertTrue(os.path.isdir('/tmp/_gar'))

    def testSimpleDirCompile2(self):
        self.mkdir('/tmp/qar')
        _('/tmp/qar', '/tmp/qqar.py')
        self.assertTrue(os.path.isdir('/tmp/qqar.py'))
        self.assertFalse(os.path.isdir('/tmp/_qar.py'))
