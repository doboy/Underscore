#  try:
#      0/0
#  except Exception as e:
#      print(type(e))

(_4,) = (0,)
(_2, _3) = (Exception, type)
try:
    _4 / _4
except _2 as _1:
    print _3(_1)
(e,) = (_1,)
