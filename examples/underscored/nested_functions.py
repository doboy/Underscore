#  def bar(a):
#      def car(b):
#          def sitar(a, c):
#              print(a, b, c)
#          print(b)
#          sitar(a+b, a)
#      car(a*2)
#  
#  bar(9)

(_8, _9) = (2, 9)

def _1(_2):

    def _3(_4):

        def _5(_6, _7):
            print (_6, _4, _7)
        print _4
        _5(_2 + _4, _2)
    _3(_2 * _8)
_1(_9)
(bar,) = (_1,)
