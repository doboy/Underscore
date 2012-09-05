#  with open('/tmp/bar', 'w') as thing:
#      print(type(thing))

(_4, _5) = ('/tmp/bar', 'w')
(_2, _3) = (open, type)
with _2(_4, _5) as _1:
    print _3(_1)
(thing,) = (_1,)
