import sys
import warnings

from StringIO import StringIO

def execute(filename):
    sys.stdout = fileOut = StringIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        execfile(filename, {'__file__': filename})
    sys.stdout = sys.__stdout__
    output = fileOut.getvalue()
    fileOut.close()
    return output
