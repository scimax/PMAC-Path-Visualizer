import math
from math import exp, sqrt, log as ln

global i15
i15=0
q0=0
def flagged_trigo(tFunc):
#     return tFunc if i15 else (lambda x: tFunc(radians(x)))
    return ( lambda x: ( tFunc(x) if i15 else tFunc(math.radians(x)) ))
def flagged_arctrigo(aFunc):
    return lambda x: (aFunc(x) if i15 else math.degrees(aFunc(x)) )
atan2 = lambda y: (math.atan2(y, q0) if i15 else math.degrees(math.atan2(y, q0)) )

cos = flagged_trigo(math.cos)
sin = flagged_trigo(math.sin)
tan = flagged_trigo(math.tan)
acos = flagged_arctrigo(math.acos)
asin = flagged_arctrigo(math.asin)
atan = flagged_arctrigo(math.atan)