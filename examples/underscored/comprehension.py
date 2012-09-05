#  print [ i+1 for i in xrange(10) if i > 2 for j in xrange(20) ]

(____, _____, ______, _______) = (1, 10, 2, 20)
(___,) = (xrange,)
print [_ + ____ for _ in ___(_____) if (_ > ______) for __ in ___(_______)]
