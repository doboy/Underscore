from operator import add

class Fibber(object):
    
    @staticmethod
    def fib(n):
        a, b = 0, 1
        for i in xrange(n):
            a, b = b, add(a, b)
        return b

print(Fibber.fib(10))
