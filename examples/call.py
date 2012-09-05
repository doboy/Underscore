def crazy_function(a, *b, **c):
    print a, b, sorted(c.items())

crazy_function(3, 6, 7, *[1, 3, 4,], d=3, z=4, **{'f': 0, 'g': 1})
