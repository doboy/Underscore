print [ i+1 for i in xrange(10) if i > 2 ]

print sorted({ j + k for j in xrange(10)
               for k in xrange(10) })

print sorted(({m: m + 1 for m in xrange(4)}).items())

