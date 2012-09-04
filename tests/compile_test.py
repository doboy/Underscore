import os
import shutil
import unittest
from underscore import _

def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)


class BaseCompileTest(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree('tmp/test')
        except:
            pass
        os.mkdir('tmp/test')

    def tearDown(self):
            shutil.rmtree('tmp/test')

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
        self.clean('tmp/test/bar')
        with self.assertRaises(ValueError) as e:
            _('tmp/test/bar')
        self.assertEquals(str(e.exception), 
                          '_: tmp/test/bar: No such file or directory')

    def testSourceSameAsDest(self):
        self.touch('tmp/test/car')
        with self.assertRaises(ValueError) as e:
            _('tmp/test/car', 'tmp/test/car')
        self.assertEquals(str(e.exception), 
                          '_: tmp/test/car and tmp/test/car are the same file')

        self.mkdir('tmp/test/far')
        with self.assertRaises(ValueError) as e:
            _('tmp/test/far', 'tmp/test/far')
        self.assertEquals(str(e.exception), 
                          '_: tmp/test/far and tmp/test/far are the same file')

    def testSourceDirDestFile(self):
        self.touch('tmp/test/foo.py')
        self.mkdir('tmp/test/zar')
        assert os.path.isdir('tmp/test/zar')
        with self.assertRaises(ValueError) as e:
            _('tmp/test/zar', 'tmp/test/foo.py')
        self.assertEquals(str(e.exception), 
                          '_: tmp/test/foo.py is a file, expected directory')
        
class HappyPathCompileTest(BaseCompileTest):
    def testSimpleFileCompile(self):
        self.touch('tmp/test/nar.py')
        _('tmp/test/nar.py')
        self.assertTrue(os.path.isfile('tmp/test/_nar.py'))

    def testSimpleFileCompile2(self):
        self.touch('tmp/test/dar.py')
        _('tmp/test/dar.py', 'tmp/test/ddar.py')
        self.assertTrue(os.path.isfile('tmp/test/ddar.py'))
        self.assertFalse(os.path.isfile('tmp/test/_dar.py'))

    def testSimpleDirCompile(self):
        self.mkdir('tmp/test/gar')
        _('tmp/test/gar')
        self.assertTrue(os.path.isdir('tmp/test/_gar'))

    def testSimpleDirCompile2(self):
        self.mkdir('tmp/test/qar')
        _('tmp/test/qar', 'tmp/test/qqar')
        self.assertTrue(os.path.isdir('tmp/test/qqar'))
        self.assertFalse(os.path.isdir('tmp/test/_qar'))
