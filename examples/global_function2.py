x = 1

def foo():
    if False:
        x = 2
    global x
    x = 3
    print x

foo()
