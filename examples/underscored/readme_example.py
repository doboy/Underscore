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

(___________, ____________, _____________) = (0, 1, 10)
(________, _________, __________) = (object, xrange, staticmethod)
from operator import add as _


class __(________):

    @__________
    def ___(____):
        (_____, ______) = (___________, ____________)
        for _______ in _________(____):
            (_____, ______) = (______, _(_____, ______))
        return ______
    (fib,) = (___,)
print __.fib(_____________)
(Fibber, add) = (__, _)
