#  try:
#      raise AssertionError, 'this is a test'
#  except:
#      print 'test passed'

(_2, _3) = ('this is a test', 'test passed')
(_1,) = (AssertionError,)
try:
    raise_1, _2
except:
    print _3
