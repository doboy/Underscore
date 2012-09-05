#  try:
#      x = 0
#      print x/x
#  except:
#      print 'Uh oh'
#  finally:
#      print 'its ok'

(_2, _3, _4) = (0, 'Uh oh', 'its ok')
try:
    try:
        _1 = _2
        print _1 / _1
    except:
        print _3
finally:
    print _4
(x,) = (_1,)
