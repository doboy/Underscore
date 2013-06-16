#  try:
#      from time import time
#  except ImportError as e:
#      from time3 import time

(___,) = (ImportError,)
try:
    from time import time as _
except ___ as __:
    from time3 import time as _

