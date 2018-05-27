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


# Start plotting
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def update_line(num, dataLine, line):
        # NOTE: there is no .set_data() for 3 dim data...
    line.set_data(dataLine[0:2, :num])
    line.set_3d_properties(dataLine[2, :num])
    return line

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Fifty lines of random 3-D lines
dat= points_to_plot.T

# Creating line object.
# NOTE: Can't pass empty arrays into 3d version of plot()
line = ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0]

# Setting the axes properties
ax.set_xlim3d([0.0, 1.0])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, 1.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 1.0])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_line, dat.shape[1], fargs=(dat, line),
                                   interval=500, blit=False)
ax.set_xlim((0,100))
ax.set_ylim((0,100))
ax.set_zlim((0,100))

#fig.show()

        """
        with open(self.pyfile, "a") as f_temp:
            f_temp.write(footer)
        
            
            