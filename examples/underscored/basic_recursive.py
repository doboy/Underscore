#  def fact(n):
#      if n <= 1:
#          return 1
#      else:
#          return n * fact(n-1)
#  
#  print fact(5)

def _(__):
    if (__ <= 1):
        return 1
    else:
        return __ * _(__ - 1)
print _(5)