#  print [ i+1 for i in xrange(10) if i > 2 ]
#  
#  print sorted({ j + k for j in xrange(10)
#                 for k in xrange(10) })
#  
#  print sorted(({m: m + 1 for m in xrange(4)}).items())
#  

(_10, _7, _8, _9) = (4, 1, 10, 2)
(_5, _6) = (xrange, sorted)
print [_1 + _7 for _1 in _5(_8) if (_1 > _9)]
print _6({_2 + _3 for _2 in _5(_8) for _3 in _5(_8)})
print _6({_4: _4 + _7 for _4 in _5(_10)}.items())
