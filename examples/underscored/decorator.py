#  def far(func):
#      print(6)
#      return func
#  
#  @far
#  def car():
#      print(9)
#  
#  print(car())

(_4, _5) = (6, 9)

def _1(_2):
    print _4
    return _2

@_1
def _3():
    print _5
print _3()
(car, far) = (_3, _1)
