#  try:
#      x = 3
#      print x[1,2:3,4]
#  except:
#      print 'it was supposed to fail'
#  

(_2, _3, _4, _5, _6) = (3, 1, 2, 4, 'it was supposed to fail')
try:
    _1 = _2
    print _1[_3, _4:_2, _5]
except:
    print _6
(x,) = (_1,)
