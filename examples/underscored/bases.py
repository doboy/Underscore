#  class a:
#      def do(self):
#          print 'a'
#          return self
#  
#  class b:
#      def run(self):
#          print 'b'
#          return self
#  
#  class c(a, b):
#      pass
#  
#  c().do().run()
#      

(_8, _9) = ('a', 'b')


class _1:

    def _2(_3):
        print _8
        return _3
    (do,) = (_2,)


class _4:

    def _5(_6):
        print _9
        return _6
    (run,) = (_5,)


class _7(_1, _4):
    pass
_7().do().run()
(a, b, c) = (_1, _4, _7)
