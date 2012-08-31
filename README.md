Underscore  [![Build Status](https://secure.travis-ci.org/Doboy/Underscore.png?branch=master)](http://travis-ci.org/Doboy/Underscore)
==========
Obfuscating code by changing the variable names to underscores

## Installation
```
pip install underscore
```

## Usage
```
$ _ file.py > _file.py
```
You can also compile through python
```python
from underscore import _

_(filename, output_filename)
```

## Example

###### Input
```python
# fib.py

from operator import add

def fib(n):
    a, b = 0, 1
    for i in xrange(n):
        a, b = b, add(a, b)
    return b

print fib(10)
```

###### Output
```python
# _fib.py

(_________,) = (xrange,)
(_______, ________, __________) = (0, 1, 10)
from operator import add as _

def __(___):
    (____, _____) = (_______, ________)
    for ______ in _________(___):
        (____, _____) = (_____, _(____, _____))
    return _____
print __(__________)
```

## Tests
There are three flavors of tests all driven by the `nosetests` framework, to add a test simply add a python file into the `examples` folder. When running the test command, `nosetests` each test will run for each file in the `examples` folder.

* `tests/diff_test.py`
  * This test makes sure that the output of the original file matches the output of the compiled file when ran.
* `tests/empty_test.py`
  * This test makes sure that there are not any empty files in the example folder.
* `tests/keyword_test.py`
  * This test makes sure that we are only using keywords and not using non `underscore` variables where possible