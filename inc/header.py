from matplotlib import use as mpluse
mpluse("TkAgg")
from Laser import *
import matplotlib.pyplot as plt

import math
from math import exp, sqrt, log as ln

# Math helper functions
i15=0
q0=0
def flagged_trigo(tFunc):
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

# Init laser object
L=Laser()

# Predefined Q variables
q161=1
q301=0
p211=0
p212=0
p213=0

# Tilt
q120=0
q121=0
q122=0

# Platform specific rotation
q130=0
q131=0
q132=0

# Rotation matrix
q140=1
q141=0
q142=0
q143=0
q144=1
q145=0
q146=0
q147=0
q148=1

# PMAC translation begins

