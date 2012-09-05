#  import ast, ast as bar
#  from ast import Add
#  from ast import Sub as sub
#  
#  print(type(Add), type(sub))
#  print(type(ast), type(bar))

(_5,) = (type,)
import ast as _1
import ast as _2
from ast import Add as _3
from ast import Sub as _4
print (_5(_3), _5(_4))
print (_5(_1), _5(_2))
(Add, ast, bar, sub) = (_3, _1, _2, _4)
