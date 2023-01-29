import numpy as np
import math
import copy
from scipy import constants

class Particle:
    """
    Class to model a neutral massive particle. Contains functinos to calculate the kinetic energy, beta value and momentum of the particle. 
    Contains functions to update the particle's position and velocity after a time step.
    
    Parameters:
    - Postion (ndarray): Particle's position vector.
    - Velocity (ndarray): Particle's velocity vector.
    - Acceleration (ndarray): Particle's acceleration vector.
    - Name (str): Name of the particle.
    - Mass (float): Particle's mass.
    - index (int): Specifies a vector component in the x, y or z direction.
    - deltaT (float): The timestep of the simulation being run. 
    Returns:
    - A statement with the particle's current parameters.

    Mass in kg, position in m, velocity in m/s, acceleration in m/s^2 
    """

    def __init__(self, Position=np.array([0,0,0], dtype=float), Velocity=np.array([0,0,0], dtype=float), Acceleration=np.array([0,0,0], dtype=float), Name='Particle Name', Mass=1.0):
        self.Name = Name
        self.position = np.array(Position,dtype=float)
        self.velocity = np.array(Velocity,dtype=float)
        self.acceleration = np.array(Acceleration,dtype=float)
        self.mass = Mass

    def __repr__(self):
        return 'Particle: %s, Mass: %s, Position: %s, Velocity: %s, Acceleration: %s'%(self.Name,self.mass,self.position, self.velocity,self.acceleration)

    def KineticEnergy(self):
        return 0.5*self.mass*np.vdot(self.velocity,self.velocity)

    def beta(self):
        return ((self.velocity)/constants.speed_of_light)
  
    def momentum(self):
        return self.mass*np.array(self.velocity,dtype=float)

    def update(self,index,deltaT):
        self.velocity[index] +=  self.acceleration[index]*deltaT
        self.position[index] +=  self.velocity[index]*deltaT

    def Velocityupdate(self,index,deltaT):
        self.velocity[index] +=  self.acceleration[index]*deltaT

    def Positionupdate(self,index,deltaT):
        self.position[index] +=  self.velocity[index]*deltaT
        
        

class Charticle(Particle):
    """
    Class to give charge parameter to particles from the Particle class to creat a charged particle. Currently set to give a proton e.g charge = 1.0
    
    Parameters:
    - Particle parameters (see above).
    - Charge (float): The charge of the particle relative to the electron charge magnitude.
    Returns:
    - A statement with the charged particle's current parameters.
    
    Charge in multiples of e, the electron charge magnitude.
    """

    def __init__(self, Position=np.array([0,0,0], dtype=float), Velocity=np.array([0,0,0], dtype=float), Acceleration=np.array([0,0,0], dtype=float), Name='Particle Name', Mass=1.0, Charge = 1.0):
        
        super().__init__(Position=Position, Velocity=Velocity, Acceleration=Acceleration, Name=Name, Mass=Mass)

        self.charge = Charge
    def __repr__(self):
        return 'Charged Particle: %s, Mass: %s, Charge: %s, Position: %s, Velocity: %s, Acceleration: %s' %(self.Name, self.mass, self.charge, self.position, self.velocity, self.acceleration)




