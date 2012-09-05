#  def bar():
#      for i in xrange(10):
#          yield i
#  
#  for z in bar():
#      print z

(_5,) = (10,)
(_4,) = (xrange,)

def _1():
    for _2 in _4(_5):
        yield _2
for _3 in _1():
    print _3
(bar, z) = (_1, _3)
