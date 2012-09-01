#  class Bar:
#      x = 1
#  
#  print Bar.x

(___,) = (1,)


class _:
    __ = ___
    (x,) = (__,)
print _.x
(Bar,) = (_,)