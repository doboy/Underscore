def crazy_function(a, b, (c, d), e=2, f=5, *g, **h):
    print a, b, c, d, e, f, g, sorted(h.items())

crazy_function(1, 2, (4, 2), 3, 4, 6, 5, q=1, w=3)
