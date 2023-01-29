import numpy as np
import pandas as pd
import math
import copy
from scipy import constants
from CosmicRayClass import CosmicRay

"""
Functions utilised in running the Atmosphere function in the AtmosphereFinal file. 

Functions:

- BunchFunction:
    Parameters: 
    - Number of particles (int): The number of particles to be simulated.
    Data Members:
    - PList (List): Contains each of the cosmic rays and the parameters they are intialised with.
    Returns:
    - PList (List)

- Direction:
    Parameters:
    - VelocityVector (ndarray): The intial velocity vector for a given cosmic ray.
    Data Members: 
    - DirectionList (List): Contains the initial direction of each of the velocity vector components. Zero or positive velocity is stored as 1. Negative velocity is stored as -1.
    Returns:
    - DirectionList (List)

- Interacted:
    Parameters:
    - InteractionValue (int): A value calculated in the CosmicRay class which, if >= 50, causes the particle to have interacted.
    Data Members:
    - Interacted (str): A statement of whether or not the cosmic ray has interacted.
    Returns:
    - Interacted (str)
"""



def BunchFunction(NumberofParticles):
    PList = []
    for i in range(1,NumberofParticles+1):
        theta = 2*math.pi*((i-1)/(NumberofParticles)) # Used below in asigning velocity vector to each cosmic ray. theta is chosen such that the cosmic ray particles each travel in differnt directions, having started at the same point.
        Proton = CosmicRay([0,8E4,0], [0.4*constants.speed_of_light*np.cos(theta), -(0.43 + (0.48*i)/NumberofParticles)*constants.speed_of_light, 0.4*constants.speed_of_light*np.sin(theta)], [0,0,0],'Proton %s'%(i),constants.proton_mass, constants.proton_mass, 1, 0, 1.0) # 80E4 is the top of the mesosphere, cosmic rays range in speed from 0.43c to 0.996c.
        PList.append(Proton)
    return(PList)

def Direction(VelocityVector):
    DirectionList = []
    for i in range(len(VelocityVector)):
        if VelocityVector[i] >= 0:
            DirectionList.append(1)
        else:
            DirectionList.append(-1)
    return(DirectionList)
    
def Interacted(InteractionValue):
    if InteractionValue >= 50:
        Interacted = 'Yes'
    else:
        Interacted = 'No'
    return(Interacted)