Underscore  [![Build Status](https://secure.travis-ci.org/Doboy/Underscore.png?branch=master)](http://travis-ci.org/Doboy/Underscore)
==========
Obfuscating code by changing the variable names to underscores

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

(________, _________, __________) = (0, 1, 10)
(_______,) = (xrange,)
from operator import add as _

def __(___):
    (____, _____) = (________, _________)
    for ______ in _______(___):
        (____, _____) = (_____, _(____, _____))
    return _____
print __(__________)
```

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

## Tests
There are three flavors of tests all driven by the `nosetests` framework, to add a test simply add a python file into the `examples` folder. When running the test command, `nosetests` each test will run for each file in the `examples` folder.

* `tests/diff_test.py`
  * This test makes sure that the output of the original file matches the output of the compiled file when ran.
* `tests/empty_test.py`
  * This test makes sure that there are not any empty files in the example folder.
* `tests/keyword_test.py`
  * This test makes sure that we are only using keywords and not using non `underscore` variables where possible
* `tests/meta_test.py` (Not ready yet)
  * This test will turn the source code into underscored code, then with the underscored code we will turn the source code into underscored code again.. and check that the `source` and `output` are the same.. I know mind blowing..

## Roadmap
This project was started on Aug 28th, 2012. And is still under development. There is lots of things to do.. here is a `TODO` list for myself
* ~~Refactor~~
* Give out warnings if users are using `exec` as this may lead to incorrect behavior.
* ~~Handle attributes~~.
* ~~Handle with statements~~
* ~~Handle exception statements~~
* Handle decorators
* ~~Handle class methods~~
* Turn the source into obfuscate code, and make sure it executes the same behavior.
* Handle the case where input has underscored variables
