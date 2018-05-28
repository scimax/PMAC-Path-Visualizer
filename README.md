# PMAC-Path-Visualizer
PMAC is a motion control language for the Turbo PMAC controller family from Delta Tau. The language combines elements from the RS-274 standard G-Code for machine instructions, and from BASIC for program logic and math. There is no direct support to graphically show all the combined moves of the connected motors.

This repository aims on graphically visualizing the paths of a pmac motion program for the specific setup used at Galatea lab, where the controller moves the focal spot of a femtosecond laser in 3D. The setup controls 5 motors:
- 3 spatial movements: X, Y, Z
- 1 power control: B-axis
- 1 polarizer: A - axis
An additional toggle is used to switch the Laser *on* and *off*.


In the first version of this project *polarization* and *writing velocity* are ignored. 

# How the program works
The visualization is done in three steps:
1. Translate the PMAC file to python file
   This is done line by line, including a header and a footer in the output file to make it executable.
2. Run the output python file
   This will export all spatial datapoints with their laser state (*on*/*off*)
3. Plot all datapoints

For simplicity step 3 is already included in step 2. The export from step 2 allows to visualize the writing paths with any other kind of software (e.g. Matlab, Gnuplot, etc.)


# How to use it
As the software is currently in development it is only available as a python script.

## Requirements
- python 3
- numpy, scipy, matplotlib, tabulate (see requirements.txt)

## Installation
1. Clone or download the repository. If you download it as a zip, unpack the archive
2. Open a command prompt in the repository directory
3. Depending on the package manager you use, run
   ```sh
   pip install -r requirements.txt
   ```
   for the python package manager, or
   ```sh
   conda install --yes --file requirements.txt
   ```
   for the conda package manager.
   
## Run
Create a new python script, e.g. myPMACPath.py, with the following content:
```py
from PMAC2Py import *
import traceback


path_to_PMAC = "Examples/LFS_Resonator_TZR_280fs_B3V3.pmc"
converter = PMAC2Py(path_to_PMAC, DEBUG=False)
converter()

with open(converter.pyfile) as f:
    try: exec(f.read())
    except: print("Got exception:", traceback.format_exc())
```
Replace the variable *path_to_PMAC* with the path to the file you want to visualize. Run it with
```
python myPMACPath.py
```

   

