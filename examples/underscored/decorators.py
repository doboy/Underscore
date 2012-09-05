#  def d1(func):
#      print 'hi'
#      return func
#  
#  def d2(word):
#      print word
#      def decor(func):
#          print 'hello'
#          return func
#      return decor
#  
#  @d1
#  @d2('test')
#  def d3():
#      print 'yo'
#  
#  d3()

(_10, _11, _8, _9) = ('yo', 'test', 'hi', 'hello')

def _1(_2):
    print _8
    return _2

def _3(_4):
    print _4

    def _5(_6):
        print _9
        return _6
    return _5

@_1
@_3(_11)
def _7():
    print _10
_7()
(d1, d2, d3) = (_1, _3, _7)
