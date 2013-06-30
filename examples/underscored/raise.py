#  try:
#      raise AssertionError('this is a test')
#  except:
#      print('test passed')

(__, ___) = ('this is a test', 'test passed')
(_,) = (AssertionError,)
try:
    raise_(__)
except:
    print ___
