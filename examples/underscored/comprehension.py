#  print [ i+1 for i in xrange(10) if i > 2 ]
#  
#  print sorted({ j + k for j in xrange(10)
#                 for k in xrange(10) })
#  
#  print sorted(({m: m + 1 for m in xrange(4)}).items())
#  

(_______, ________, _________, __________) = (1, 10, 2, 4)
(_____, ______) = (xrange, sorted)
print [_ + _______ for _ in _____(________) if (_ > _________)]
print ______({__ + ___ for __ in _____(________) for ___ in _____(________)})
print ______({____: ____ + _______ for ____ in _____(__________)}.items())
