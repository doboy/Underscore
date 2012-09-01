def far(func):
    print 6
    return func

@far
def car():
    print 9

print car()
