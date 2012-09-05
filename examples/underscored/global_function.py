#  x = 1
#  
#  def foo():
#      global x
#      print(x)
#      x = 3
#      print(x)
#  
#  foo()

(_4, _5) = (1, 3)
_1 = _4

def _2():
    global _1
    print _1
    _1 = _5
    print _1
_2()
(foo, x) = (_2, _1)
