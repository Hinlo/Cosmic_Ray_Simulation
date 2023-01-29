import numpy as np
import math
import copy
import random
import time
from scipy import constants
from Particle import Charticle
from CosmicRaySupportFunctions import StoppingForce, NonRelativisticStoppingForce, ForceDirectionCheck

 

class CosmicRay(Charticle):
    """
    Imports Charticle and Particle from Particle.py, Imports functions from the CosmicRaySupportFunctions file.
    Class to create cosmic rays using charged particles by introducing interaction probability, relativistic mass and a value for the lorentz factor gamma.
    The class also contains a update functions for interacting and non-interacting cosmic ray parameters.

    Parameters:
    - Charticle Parameters (See Charticle class in Particle.py)
    - RestMass (float): The initial mass of a particle. This value is constant and used to update the particles mass due to it's relativistic speed.
    - Interact (int): a value to specify whether the particle has interacted or not. A particle has interacted if Interact >= 50 
    - Gamma (float): a value for the lorentz factor of the particle in the y direction calculated using its y velocity magnitude. 
    returns:
    - A statement with the Cosmic Ray's current parameters.

    RestMass in kg, Interact and Gamma have no units.
    """

    def __init__(self, Position=np.array([0,0,0], dtype=float), Velocity=np.array([0,0,0], dtype=float), Acceleration=np.array([0,0,0], dtype=float), Name='Particle Name', RestMass = 1.0, Mass=1.0, Charge = 1.0, Interact = 0, Gamma = 1.0):
        
        super().__init__(Position=Position, Velocity=Velocity, Acceleration=Acceleration, Name=Name, Mass=Mass, Charge = Charge)
        self.restmass = RestMass
        self.interact = Interact
        self.gamma = Gamma
        
    def __repr__(self):
        return 'Cosmic Ray: %s, Mass: %s, Charge: %s, Position: %s, Velocity: %s, Acceleration: %s, Interact: %s' %(self.Name, self.mass, self.charge, self.position, self.velocity, self.acceleration, self.interact)



    # Function to update parameters of cosmic rays 
    def CosmicRayUpdate(self, deltaT, PositionList, VelocityList, AccelerationList, ListofDirections):
        Beta = self.beta() # Initialise beta, required in the stopping force functions.
        for i in range(len(self.velocity)): # Run the update function in each of the x, y and z directions.
            if self.interact >= 50: # Runs if particle has interacted. Here the particle is stopped.
                self.velocity[i] = 0
                self.acceleration[i] = 0
                PositionList[i].append(self.position[i])
                VelocityList[i].append(self.velocity[i])
                AccelerationList[i].append(self.acceleration[i])
            else: # Particle is moves through the atmosphere and experiences electronic stopping force.
                PositionList[i].append(self.position[i])
                VelocityList[i].append(self.velocity[i])
                if np.abs(self.velocity[i]) <= 2.74E6: # minimum speed before bethe stopping power equation breaks due to negative natural log. We must stop the cosmic ray at this point.
                    AccelerationList[i].append(self.acceleration[i])
                    self.velocity[i] = 0
                    self.acceleration[i] = 0

                else:
                    if np.abs(self.velocity[i]) >= 1E7: # Runs if particle moves at relativistic speeds in a given direction.
                        Force = StoppingForce(1.67E25,self.charge,Beta[i],1.36E-17) # Using two times mesosphere electron density; particles fall just into the stratosphere so density should be slighlt higher than mesosphere electron density. Using mean excitation potential of air.              
                    else: # Runs if particle moves at non-relativistic speeds in a given direction.
                        Force = NonRelativisticStoppingForce(1.67E25,self.charge,self.velocity[i],1.36E-17) # Using two times mesosphere electron density; particles fall just into the stratosphere so density should be slighlt higher than mesosphere electron density. Using mean excitation potential of air.            

                    AccelerationCalc = (Force/self.mass) # Calculate the decceleration of the particle due to the stopping force.
                    self.acceleration[i] = ForceDirectionCheck(ListofDirections[i],AccelerationCalc)                
                    AccelerationList[i].append(self.acceleration[i])
                    self.Velocityupdate(i,deltaT)
                    
                    if ListofDirections[i] == 1 and self.velocity[i] < 0: # Check if the particle has changed direction due to stopping force, if so stop it in that direction. 
                        self.velocity[i] = 0
                        self.acceleration[i] = 0 
                        self.Positionupdate(i,deltaT)
                    elif ListofDirections[i] == -1 and self.velocity[i] > 0: # Check if the particle has changed direction due to stopping force, if so stop it in that direction. 
                        self.velocity[i] = 0
                        self.acceleration[i] = 0 
                        self.Positionupdate(i,deltaT)
                    else:
                        self.Positionupdate(i,deltaT) # This runs if particle has not been stopped yet.

    # Function to check whether a cosmic ray has interacted and recalculate the Interact value if it has not.
    def InteractionCheck(self):
        if self.interact >= 50: # Particle has already interacted if Interact >= 50
            pass
        else:
            InteractValues = []
            for i in range(len(self.velocity)): # Calculate a value for Interact in x,y,z directions independently.
                if i == 1:                                                                             # Interaction probability is proportional distance travelled. 
                    InteractCalc = round(np.random.normal(0,43)*(np.abs(8E4 - self.position[i])/(700)))# The calculation is set so that the average particle decays after travelling 700m.
                else: # x and z position components start at 0m and so run through this. Y position starts at 8E4 and so runs above.
                    InteractCalc = round(np.random.normal(0,43)*(np.abs(self.position[i])/(700)))
                InteractValues.append(InteractCalc)                                         
            self.interact = max(InteractValues) # If the particle reaches the interaction value in any direction, it should interact, so the maximum value of Interaction is chosen.
    # Function to calculate the lorentz factor for the cosmic ray.
    def GammaUpdate(self):
        BetaValue = abs(self.velocity[1])/constants.speed_of_light# np.linalg.norm(self.velocity)/constants.speed_of_light # Calculate a value for Beta: velocity magnitude divided by speed of light in a vacuum.
        self.gamma = (1/(math.sqrt(1 - BetaValue*BetaValue)))
        return (self.gamma)
    # Function to calculate the relativistic mass of the cosmic ray.
    def MassUpdate(self):
        self.mass = self.gamma*self.restmass
        return (self.mass)
    # Function to calculate the total energy of the particle.
    def ParticleEnergyUpdate(self):
        Energy = self.mass*constants.speed_of_light*constants.speed_of_light
        return (Energy)

