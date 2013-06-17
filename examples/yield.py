def bar():
    for i in xrange(10):
        yield i

for z in bar():
    print(z)
