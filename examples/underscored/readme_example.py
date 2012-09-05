#  from operator import add
#  
#  class Fibber(object):
#      
#      @staticmethod
#      def fib(n):
#          a, b = 0, 1
#          for i in xrange(n):
#              a, b = b, add(a, b)
#          return b
#  
#  print(Fibber.fib(10))

(_11, _12, _13) = (0, 1, 10)
(_10, _8, _9) = (staticmethod, object, xrange)
from operator import add as _1


class _2(_8):

    @_10
    def _3(_4):
        (_5, _6) = (_11, _12)
        for _7 in _9(_4):
            (_5, _6) = (_6, _1(_5, _6))
        return _6
    (fib,) = (_3,)
print _2.fib(_13)
(Fibber, add) = (_2, _1)
