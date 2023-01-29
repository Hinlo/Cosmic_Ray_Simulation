import numpy as np
import pandas as pd
import math
import copy
from scipy import constants
from pytest import approx
from CosmicRayClass import CosmicRay
from AtmosphereSupportFunctions import BunchFunction, Direction, Interacted
from CosmicRaySupportFunctions import StoppingForce, NonRelativisticStoppingForce, ForceDirectionCheck

"""
This file contains test functions for each of the testable functions used in the simulation. Each file is docstringed individually.
To initialise test: open terminal: view -> Terminal, once terminal loads, type in pytest, this runs pytest across all files in the folder.
"""
TestProton = CosmicRay([0,8E4,0], [0,-0.6*constants.speed_of_light,0], [0,0,0],'Proton', constants.proton_mass, constants.proton_mass, 1.0, 0, 1)
StationaryTestProton = CosmicRay([0,8E4,0], [0,0,0], [0,0,0],'Proton', constants.proton_mass, constants.proton_mass, 1.0, 0, 1)



# AtmosphereSupportFunctions Tests:
def test_BunchFunction(): 
    """
    Check that a bunch containing a single particle returns a list of length one and the particle is given the maximum velocity vector 
    """
    ListofOne = BunchFunction(1)
    assert len(ListofOne) == 1
    assert np.all(ListofOne[0].velocity == [0.4*constants.speed_of_light*np.cos(2*math.pi*(0)), -(0.43 + (0.48))*constants.speed_of_light, 0.4*constants.speed_of_light*np.sin(2*math.pi*(0))]) #CosmicRay([0,8E4,0], , [0,0,0],'Proton 1',constants.proton_mass, constants.proton_mass, 1, 0, 1.0) 
    
def test_Direction (): 
    """ 
    Check that particles direction is correctly identified, the test proton has positive X and Z velocity and negative Y velocity.
    """
    assert Direction(TestProton.velocity) == [1,-1,1]

def test_Interacted():
    """
    To have interacted return 'Yes', a particle must have an interact value of 50 or greater.
    """
    assert Interacted(0) == 'No'
    assert Interacted(49) == 'No'
    assert Interacted(50) == 'Yes'
    assert Interacted(99) == 'Yes'


# CosmicRayClass Tests:
def test_GammaUpdate():
    """
    For a particle with speed = 0.6c, gamma should be = 1.25.
    """
    assert TestProton.GammaUpdate() == 1.25 
def test_MassUpdate():
    """
    For a particle with gamma = 1.25, relativistic mass = 1.25*restmass.
    """
    assert TestProton.MassUpdate() == 1.25*constants.proton_mass
def test_ParticleEnergyUpdate():
    """
    Stationary particle should return rest energy, moving particle
    with relativistic mass = 1.25restmass should have 
    energy == 1.25*restmass*c^2.
    """
    assert StationaryTestProton.ParticleEnergyUpdate() == TestProton.restmass*constants.speed_of_light*constants.speed_of_light
    assert TestProton.ParticleEnergyUpdate() == 1.25*TestProton.restmass*constants.speed_of_light*constants.speed_of_light


# CosmicRaySupportFunctions Tests:
def test_Stoppingforce(): 
    """
    Check that relativistic stopping force gives correct value
    for a given input.
    """
    assert StoppingForce(5.3E25,1,0.9,1.36E-17)*1E15 == approx(-5.33, rel = 0.01) # Multiply by 1e15 as approx only has accuracy of 1E-12
def test_NonRelativisticStoppingforce():
    """
    Check that non-relativistic stopping force gives correct 
    value for a given input.
    """
    assert NonRelativisticStoppingForce(5.3E25,1,5E6,1.36E-17)*1E12 == approx(-1.87, rel = 0.01) # Multiply by 1e15 as approx only has accuracy of 1E-12
def test_ForceDirectionCheck(): 
    """
    Check that forcedirection is only switched if particle 
    moves in the negative direction along a given axis.
    """
    assert ForceDirectionCheck(1,1) == 1
    assert ForceDirectionCheck(-1,1) == -1


# Particle Tests:
def test_KineticEnergy(): 
    """
    Stationary particle should have zero kinetic energy. 
    Test proton should have kinetic energy value 3.38E-11 
    (considering relativistic mass of 1.25restmass).
    """
    assert StationaryTestProton.KineticEnergy() == 0.0
    assert TestProton.KineticEnergy()*1E11 == approx(3.382, 0.001)
def test_beta():
    """
    Check that Stationary particles have beta value of zero.
    Check that moving particle has correct beta array.
    """
    assert np.all(StationaryTestProton.beta() == [0,0,0])
    assert np.all(TestProton.beta() == [0,-0.6,0])
def test_momentum():
    """
    Check that stationary particles have zero momentum.
    Check that moving particle has correct momentum magnitude.
    """
    assert np.all(StationaryTestProton.momentum() == [0,0,0])
    assert np.linalg.norm(TestProton.momentum())*1E19 == approx(3.758,0.001)



