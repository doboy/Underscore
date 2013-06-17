import sys
import warnings

try:
    from StringIO import StringIO
except:
    # Python 3 support
    from io import StringIO

# Python 3 does not have execfile, so just create one
def xfile(afile, globalz=None, localz=None):
    with open(afile, "r") as fh:
        exec(fh.read(), globalz, localz)

def execute(filename):
    sys.stdout = fileOut = StringIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        xfile(filename, {'__file__': filename})
    sys.stdout = sys.__stdout__
    output = fileOut.getvalue()
    fileOut.close()
    return output
