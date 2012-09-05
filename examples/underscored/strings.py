#  x = '1''''a-
#  multi-
#  lined- string!
#  '''
#  
#  y = 'c'
#  z = x + y
#  print(x, y, z)

(_4, _5) = ('1a-\nmulti-\nlined- string!\n', 'c')
_1 = _4
_2 = _5
_3 = _1 + _2
print (_1, _2, _3)
(x, y, z) = (_1, _2, _3)
