
points_to_plot = L.exportHistory()
sections_to_plot = [sec.T for sec in points_to_plot if sec[0,3]==1]


# Start plotting
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from helper_3d_axes import set_axes_equal

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Creating line object.
# NOTE: Can't pass empty arrays into 3d version of plot()
for dat in sections_to_plot:
    line = ax.plot(dat[0, :], dat[1, :], dat[2, :])[0]

# Setting the axes properties
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_title('3D Test')
set_axes_equal(ax)
plt.show()