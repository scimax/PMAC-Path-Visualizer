import tempfile
from PMACParser import *
import os
from IPython.display import HTML, display
import tabulate as tb

class PMAC2Py:
    def __init__(self, filepath, DEBUG=False):
        self.filepath = filepath
        self.DEBUG=DEBUG
        self.pyfile = tempfile.mkstemp(dir=os.getcwd())[1]
        self.parser = PMACParser()
        
    def __call__(self):    
        self.initHeader()
        self.processFile()
        self.footer()
        
    def initHeader(self):
        header= """
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
p213=0

# PMAC translation begins
"""
        with open(self.pyfile,"w") as f_temp:
            f_temp.write(header)
            
    def processFile(self):
        with open(self.pyfile,"a") as f_temp, open(self.filepath, "r") as  pmc_file:
#             print([self.parser.convertLine(line) for line in pmc_file.readlines() ])
            f_temp.write(
                "".join(
                    [self.parser.convertLine(line) for line in pmc_file.readlines() ]
                    )
            )
        if self.DEBUG:
            with open(self.filepath, "r") as pmc_file:
                processed_list = [[line, self.parser.convertLine(line)] for line in pmc_file.readlines()]
                # for i,line in enumerate(pmac_str.split("\n")):
                #     print(i, "   ",  line, "   ", pmc.convertLine(line))
                tb.PRESERVE_WHITESPACE = True
                table_str=(tb.tabulate(
                    processed_list,
                    showindex="always",
                    headers=["PMC", "python"],
                ))
                print(table_str)
                
    def footer(self):
        footer = """

points_to_plot = L.exportHistory()
sections_to_plot = [sec.T for sec in points_to_plot if sec[0,3]==1]


# Start plotting
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Creating line object.
# NOTE: Can't pass empty arrays into 3d version of plot()
for dat in sections_to_plot:
    line = ax.plot(dat[0, :], dat[1, :], dat[2, :])[0]

# Setting the axes properties
ax.set_xlim3d([0.0, 1.0])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, 1.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 1.0])
ax.set_zlabel('Z')

ax.set_title('3D Test')

ax.set_xlim((0,200))
ax.set_ylim((0,200))
ax.set_zlim((0,200))
plt.show()
        """
        with open(self.pyfile, "a") as f_temp:
            f_temp.write(footer)
        
            
            