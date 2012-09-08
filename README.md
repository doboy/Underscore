Underscore  [![Build Status](https://secure.travis-ci.org/Doboy/Underscore.png?branch=master)](http://travis-ci.org/Doboy/Underscore)
==========
Obfuscating code by changing the variable names to underscores

## Example

###### Input
```python
# fib.py

from operator import add

class Fibber(object):
    
    @staticmethod
    def fib(n):
        a, b = 0, 1
        for i in xrange(n):
            a, b = b, add(a, b)
        return b

print Fibber.fib(10)
```

###### Output
```python
# _fib.py

(___________, ____________, _____________) = (0, 1, 10)
(________, _________, __________) = (object, xrange, staticmethod)
from operator import add as _


class __(________):

    @__________
    def ___(____):
        (_____, ______) = (___________, ____________)
        for _______ in _________(____):
            (_____, ______) = (______, _(_____, ______))
        return ______
    (fib,) = (___,)
print __.fib(_____________)
(Fibber, add) = (__, _)
```

## Installation
```
pip install underscore
```

Support for `python2.6` and `python2.7`

## Usage
```
Usage: _ [options] src [dest]

Options:
  -h, --help      show this help message and exit
  -o, --original  write out the original file as a comment to the compiled
                  code
  -v, --verbose
```
You can also compile through python
```python
from underscore import _

_(filename, output_filename)
```

## Development
##### Setup
```python setup.py develop```

##### Running Tests
```python setup.py nosetests```

##### Tests
* `tests/compile_test.py`
  * This test makes sure that all argument combinations for the comandline tool works properly
* `tests/diff_test.py`
  * This test compiles python files in `example/` into `example/underscored` then runs both version to check that their outputs are equivalent.
* `tests/meta_test.py` (Not ready yet)
  * This test will turn the source code into underscored code, then with the underscored code we will turn the source code into underscored code again.. and check that the `source` and `output` are the same.. I know mind blowing..

##### TODO
* Give out warnings if users are using `exec` as this may lead to incorrect behavior.
* Write the `meta_test.py` described above.
* Module doc-string to work