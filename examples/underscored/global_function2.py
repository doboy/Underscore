#  x = 1
#  
#  def foo():
#      if False:
#          x = 2
#      global x
#      x = 3
#      print x
#  
#  foo()

(_____, ______, _______) = (1, 2, 3)
(____,) = (False,)
_ = _____

def __():
    if ____:
        _ = ______
    global _
    _ = _______
    print _
__()
(foo, x) = (__, _)