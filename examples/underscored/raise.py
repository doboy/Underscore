#  try:
#      raise AssertionError, 'this is a test', 'xx'
#  except:
#      print 'test passed'

(__, ___, ____) = ('this is a test', 'xx', 'test passed')
(_,) = (AssertionError,)
try:
    raise_, __, ___
except:
    print ____
