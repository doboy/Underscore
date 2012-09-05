#  def crazy_function(a, *b, **c):
#      print a, b, sorted(c.items())
#  
#  crazy_function(3, 6, 7, *[1, 3, 4,], d=3, z=4, **{'f': 0, 'g': 1})

(_10, _11, _12, _13, _6, _7, _8, _9) = (1, 'f', 'g', 0, 3, 6, 7, 4)
(_5,) = (sorted,)

def _1(_2, *_3, **_4):
    print _2, _3, _5(_4.items())
_1(_6, _7, _8, d=_6, z=_9, *[_10, _6, _9], **{_11: _13, _12: _10})
(crazy_function,) = (_1,)
