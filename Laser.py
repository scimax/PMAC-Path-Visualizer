from enum import Enum
import numpy as np
class Laser:
    def __init__(self, ax=None):
        self.status = False #Status is either Off or On
        self.moveRel = True # else: move type is abs
        self.moveStyle = Mode.LINEAR
        self.home = np.array([0.,0.,0., 0.], dtype='float64')
        self.pos = np.array([0.,0.,0., 0.], dtype='float64')
        self.posHistory = [np.zeros(4)]
        
    def move(self, x,y,z):
        if self.moveRel:
            a = self.pos + np.array([x,y,z, 0])
        else:
            a = self.home + np.array([x,y,z, 0])
        a[3] = bool(self.status)
#         print("Move:",a)
        self.posHistory.append(a)
        self.pos = a
        return a[0], a[1], a[2]
    
    def arcMove(self, x, y, r):
        # TODO for Pieter
        pass
    
    def homing(self):
        self.home = self.pos
        
    def exportHistory(self):
        positions = np.array(self.posHistory)
        ind_split =  np.where( np.abs(np.diff(positions[:,3])) != 0.)[0]
        pos_on_off = np.split(positions, ind_split+1)
        np.save("positions.npy", pos_on_off)
        return np.array(pos_on_off)
    
    def toggle_on_off(self, new_state):
        '''new_state: boolean'''
        if self.status != new_state:
            self.status = new_state
            self.move(0,0,0)
    
class Mode(Enum):
    LINEAR= 0
    CIRCLE= 1
    