import sys
import warnings

try:
    from StringIO import StringIO
except:
    # Python 3 support
    from io import StringIO

def execute(filename):
    sys.stdout = fileOut = StringIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        execfile(filename, {'__file__': filename})
    sys.stdout = sys.__stdout__
    output = fileOut.getvalue()
    fileOut.close()
    return output
