def bar():
    for i in range(10):
        yield i

for z in bar():
    print(z)
