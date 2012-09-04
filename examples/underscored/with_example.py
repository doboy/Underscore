#  with open('/tmp/bar', 'w') as thing:
#      print type(thing)

(____, _____) = ('/tmp/bar', 'w')
(__, ___) = (open, type)
with __(____, _____) as _:
    print ___(_)
(thing,) = (_,)
