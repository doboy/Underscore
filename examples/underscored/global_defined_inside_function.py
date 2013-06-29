#  def foo():
#      global x
#      x = 3
#
#  foo()
#  print(x)

(___,) = (3,)

def _():
    global __
    __ = ___
_()
print __
(foo, x) = (_, __)
