x = lambda y, *z, **a: (y, z, sorted(a.items()))

print(x(1, 2, 4, 5, 2, k=3, r=4, l=2))
