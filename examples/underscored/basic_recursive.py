#  def fact(n):
#      if n <= 1:
#          return 1
#      else:
#          return n * fact(n-1)
#  
#  print(fact(5))

(_3, _4) = (1, 5)

def _1(_2):
    if (_2 <= _3):
        return _3
    else:
        return _2 * _1(_2 - _3)
print _1(_4)
(fact,) = (_1,)
