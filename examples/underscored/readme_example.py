#  from operator import add
#  
#  class Fibber(object):
#      
#      def fib(n):
#          a, b = 0, 1
#          for i in xrange(n):
#              a, b = b, add(a, b)
#          return b
#  
#  print Fibber().fib(10)

(__________, ___________, ____________) = (0, 1, 10)
(________, _________) = (object, xrange)
from operator import add as _


class __(________):

    def ___(____):
        (_____, ______) = (__________, ___________)
        for _______ in _________(____):
            (_____, ______) = (______, _(_____, ______))
        return ______
    (fib,) = (___,)
print __().fib(____________)
(Fibber, add) = (__, _)