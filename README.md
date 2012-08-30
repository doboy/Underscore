Underscore
==========
Obfuscating code by changing the variable names to underscores

## Installation
```
pip install underscore
```

## Usage
```
$ _ [file] > _file.py
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

def fib(n):
    a, b = 0, 1
    for i in xrange(n):
        a, b = b, a + b
    return b

print fib(10)
```

###### Output
```python
# _fib.py

def _(_):
    (__, ___) = (0, 1)
    for ____ in xrange(_):
    (__, ___) = (___, __ + ___)
    return ___
print _(10)
```

## Tests
```
nosetests
```