import numpy as np
import pandas as pd
import math
import copy
from scipy import constants

"""
Functions utilised in running the CosmicRay class in the CosmicRayClass file. 

Functions:

- StoppingForce:
    Parameters: 
    - eDensity (float): The electron density of the atmosphere (different in different atmospheric layers).
    - charge (float): The charge of the particle the force is applied to, relative to the electron charge magnitude.
    - beta (float): The beta value of the particle, calculated by dividing its speed by the speed of light in a vacuum.
    - V_excitation (float): The mean excitation potential of air in the atmosphere. 
    Data Members:
    - StoppingForce (float): The electronic stopping force acting on the particle as a result of its motion throught the atmosphere. Calculated using the Bethe Stopping power formula.
    Returns:
    - StoppingForce (float)

- NonRelativisticStoppingForce:
    Parameters: 
    - eDensity (float): The electron density of the atmosphere (different in different atmospheric layers).
    - charge (float): The charge of the particle the force is applied to, relative to the electron charge magnitude.
    - beta (float): The beta value of the particle, calculated by dividing its speed by the speed of light in a vacuum.
    - V_excitation (float): The mean excitation potential of air in the atmosphere. 
    Data Members:
    - NonRelStoppingForce (float): The electronic stopping force acting on the particle as a result of its (at non-relativistic speeds) motion throught the atmosphere. Calculated using the non-relativistic Bethe Stopping power formula.
    Returns:
    - NonRelStoppingForce (float)

- ForceDirectionCheck:
    Parameters:
    - DirectionListComponent(int): An integer representing motion in the positive or negative direction, given by +1 or -1 respectively. Zero motion is given a direction of +1.
    - AccelerationComponent(float): The acceleration value in a given direction (x, y or z), calculated using the stopping force calculated prior.
    Returns:
    - +/-AccelerationComponent (float): The function will switch the direction of the acceleration component such that it always opposes the direction of particle motion and thus slows the particle.
"""

def StoppingForce(eDensity,charge,beta,V_excitation): # Note beta is different for each x, y, z direction.
    t1 = (4*math.pi)/(constants.electron_mass*constants.speed_of_light*constants.speed_of_light)
    t2 = (eDensity*charge*charge)/(beta*beta)
    t3 = (constants.elementary_charge*constants.elementary_charge)/(4*math.pi*constants.epsilon_0)
    ln = np.log((2*constants.electron_mass*constants.speed_of_light*constants.speed_of_light*beta*beta)/(V_excitation*(1-beta*beta)))
    t4 = ln - beta*beta
    StoppingForce = -t1*t2*t3*t3*t4 # Stopping force is a large calculation and so has been done in steps above to ensure no mistakes were made.
    return(StoppingForce)

def NonRelativisticStoppingForce(eDensity,charge,ispeed,V_excitation):
    t1 = (4*math.pi*eDensity*charge*charge)/(constants.electron_mass*ispeed*ispeed)
    t2 = (constants.elementary_charge*constants.elementary_charge)/(4*math.pi*constants.epsilon_0)
    t3 = np.log((2*constants.electron_mass*ispeed*ispeed)/(V_excitation))
    NonRelStoppingForce = -t1*t2*t2*t3 # Stopping force is a large calculation and so has been done in steps above to ensure no mistakes were made.
    return(NonRelStoppingForce)

def ForceDirectionCheck(DirectionListComponent,AccelerationComponent):
    if DirectionListComponent >= 0:
        return(AccelerationComponent)
    else: 
        return(-AccelerationComponent) # The negative acceleration changes direction if direction of motion is negative so that a positive acceleration is applied in this case, thus slowing the particle.

