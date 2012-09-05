#  print 3 if False else 5 if True else 5
#  print 3 if True else 5

(_3, _4) = (3, 5)
(_1, _2) = (False, True)
print _3 if _1 else _4 if _2 else _4
print _3 if _2 else _4
