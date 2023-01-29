import numpy as np
import pandas as pd
import math
import copy
import random
from scipy import constants
from CosmicRayClass import CosmicRay
from AtmosphereSupportFunctions import BunchFunction, Direction, Interacted

"""
Imports CosmicRay class and functions from the  AtmosphereSupportingFunctions file and uses these to update the parameters of each cosmic ray in the initial bunch, at each time
step over a given run time. The lists of parameter values are made into a dictionary and subsequently into a dataframe which is then pickled, saving to the 'Data' Folder.

Parameters:
- RunTime (float): The time, in seconds, for which the simulation runs.
- NumberofCosmicRays (int): The number of cosmic rays to be simulated. Sensible values range from 1-1000.
- InteractionOnOff (string): A parameter to dictate whether cosmic rays in the simulation are able to interact or not.

Data Members:
- time (float): The current time value in the simulation, ranging from 0 to RunTime in steps of deltaT. 
- deltaT(float): The timestep used in the simulation. It is set as 1/1000th of the RunTime value.
- TimeList (List): Contains the current time at each timestep. Is included in the dataframe for each particle.
- InteractList (List): Contains a statement on whether a particle has interacted at each timestep. For interacting particles this is 'No' or 'Yes'. For non-interacting 
particles, this is 'N/A'. Is included in the dataframe for each particle.
- ParticleEnergyList (List): Contains the total energy of a particle at each timestep. Is included in the dataframe for each particle.
- PositionList (List): Contains the position vector of the particle at each timestep. Is included in the dataframe for each particle.
- VelocityList (List): Contains the velocity vector of the particle at each timestep. Is included in the dataframe for each particle. 
- AccelerationList (List): Contains the acceleration vector of the particle at each timestep. Is included in the dataframe for each particle.
- SpeedList (List): Contains the velocity magnitudes of the particle at each timestep. Is included in the dataframe for each particle.
- List of Directions (List): Contains the initial direction of each of the velocity vector components. Zero or positive velocity is stored as 1. Negative velocity is stored as -1.

Returns: 
- Bunch (List):Contains each of the cosmic rays in the bunch with their final state parameters. 
"""

def Atmosphere(RunTime, NumberofCosmicRays, InteractionOnOff): 
    Bunch = BunchFunction(NumberofCosmicRays) # Initialise the bunch of cosmic rays.
    interactionOnOff = InteractionOnOff # The if-else statement selects whether interactions will or won't be simulated.
    if interactionOnOff == 'I' or interactionOnOff == 'i':
        Update = 1
    else:
        Update = 0
    
    for j in range(NumberofCosmicRays): # As cosmic rays do not interact with each other, the simulation is run sequentially for each cosmic ray in the bunch. 

        time = 0.0 # Initialise all data members.
        deltaT = 0.001*RunTime
        TimeList = []
        InteractList = []
        ParticleEnergyList = []
        PositionList = [[],[],[]]
        VelocityList = [[],[],[]]
        AccelerationList = [[],[],[]]
        SpeedList = []
        ListofDirections = Direction(Bunch[j].velocity)

        for _ in np.arange(0, RunTime, deltaT): # Run the simulation for the given cosmic ray over the RunTime, updating every timestep - deltaT.
            TimeList.append(time) # Append values for this time-step to each data member. These are done before updating the cosmic ray parameters so that intial parameters are recorded.
            SpeedList.append(np.linalg.norm(Bunch[j].velocity))
            Bunch[j].GammaUpdate() # Calculate gamma for cosmic ray at its current speed.
            Bunch[j].MassUpdate() # Use gamma to calculate relativistic mass of cosmic ray.
            ParticleEnergyList.append(Bunch[j].ParticleEnergyUpdate()) 

            if Update == 1: # If statment runs if cosmic rays can interact.
                InteractList.append(Interacted(Bunch[j].interact)) 
                Bunch[j].CosmicRayUpdate(deltaT, PositionList, VelocityList, AccelerationList, ListofDirections) # Run the CosmicRay class CosmicRayInteractionUpdate Function.
                Bunch[j].InteractionCheck() # Run the CosmicRay class InteractionCheck function.
            else: # Else statement runs if cosmic rays cannot interact.
                Bunch[j].CosmicRayUpdate(deltaT, PositionList, VelocityList, AccelerationList, ListofDirections) # Run the CosmicRay class CosmicRayUpdate function.
                InteractList.append('N/A')
            
            time += deltaT # Add one timestep to the time before repeating the loop.
        CosmicRayData = {'Particle':j+1, 'Time [s]':TimeList, 'Interacted?':InteractList, 'Y Energy [J]':ParticleEnergyList, # Create a dictionary with the parameters for the cosmic ray at each timestep.
                        'Speed [m/s]':SpeedList, 'X Pos [m]':PositionList[0], 'Y Pos [m]':PositionList[1],'Z Pos [m]':PositionList[2],
                        'X Vel [m/s]':VelocityList[0], 'Y Vel [m/s]':VelocityList[1], 'Z Vel [m/s]':VelocityList[2],
                        'X Acc [m/s^2]':AccelerationList[0], 'Y Acc [m/s^2]':AccelerationList[1], 'Z Acc [m/s^2]':AccelerationList[2]}
        CosmicRayDataFrame = pd.DataFrame(CosmicRayData) # Convert the dictionary to a dataframe for the cosmic ray.
        CosmicRayDataFrame.to_pickle('Data/Cosmic_Ray_Data_%s.csv' %(j+1)) # Pickle and save the dataframe to the Data folder. The data frames are saved with the cosmic ray's number in the bunch.
        percent = round((j+1)/(len(Bunch))*100, 1) # A calculation to print percentage completion of the simulation. This prints after each cosmic ray has been simulated.
        print('Simulation is %s %% complete' %(percent))
    return(Bunch) # Return the bunch of cosmic rays, now with their final parameters.
    
