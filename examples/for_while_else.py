i = 10
while i > 0:
    i -= 1
    if i % 2:
        continue
    print i
else:
    print 3

for i in xrange(10):
    print i
    if i == 4:
        break
else:
    print 5
