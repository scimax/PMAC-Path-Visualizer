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
        print("Move:",a)
        self.posHistory.append(a)
        self.pos = a
        return x,y,z
    
    def arcMove(self, x, y, r):
        # TODO for Pieter
        pass
    
    def homing(self):
        self.home = self.pos
        
    def exportHistory(self):
        positions = np.array(self.posHistory)
        ind_split =  np.where( np.abs(np.diff(positions[:,3])) != 0.)[0]
        ext_ind_split = [0, *ind_split, positions.shape[0]]
        pos_on_off = [ positions[i:(j+1) ] for i,j in zip( ext_ind_split[:-1], ext_ind_split[1:] ) ]
        np.save("positions.npy", pos_on_off)
#         np.save("positions.npy", positions)
        return pos_on_off
    
    def toggle_on_off(self, new_state):
        '''new_state: boolean'''
        if self.status != new_state:
            print(self.posHistory[-1])
            self.status = new_state
            self.pos[3]= new_state
            b = np.copy(self.pos)
            b[3] = new_state
            print(self.pos)
            self.posHistory.append(b)
            print(self.posHistory[-1])
    
class Mode(Enum):
    LINEAR= 0
    CIRCLE= 1
    