x = 1

def foo():
    global x
    print(x)
    x = 3
    print(x)

foo()
