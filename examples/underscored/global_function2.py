#  x = 1
#  
#  def foo():
#      if False:
#          x = 2
#      global x
#      x = 3
#      print(x)
#  
#  foo()

(_5, _6, _7) = (1, 2, 3)
(_4,) = (False,)
_1 = _5

def _2():
    if _4:
        _1 = _6
    global _1
    _1 = _7
    print _1
_2()
(foo, x) = (_2, _1)
