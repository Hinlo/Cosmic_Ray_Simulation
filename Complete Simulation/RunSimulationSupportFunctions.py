import numpy as np
import pandas as pd
import math
import copy
import random
from scipy import constants
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
Functions utilised in running the RunSimulation file. 

Functions:

- DataRead:
    Parameters:
    - Number of Particles (int): The number of cosmic rays in the simulation.
    - Dataframes (List): Contains the dataframe of each cosmic ray in the simulation.
    DataMembers:
    - Data (DataFrame): The dataframe of a given particle. This is appended to the DataFrames list.
    - DataReadPercent (float): percentage complete value printed to show how much of the data read has been completed.
    
- DataFrameShow:
    Parameters:
    - Dataframes (List): Contains the dataframe of each cosmic ray in the simulation.
    DataMembers:
    - Answer (str, User Input): A statment allowing the user to decide whether or not to look at any cosmic ray dataframe.
    - ParticleNumber (int, User Input): A value allowing the user to select which cosmic ray dataframe they would like to look at.

- TrajectoryPlot, DecelerationPlot, EnergyLossPlot:
    Parameters:
    - Dataframes (List): Contains the dataframe of each cosmic ray in the simulation.
    - Number of Particles (int): The number of cosmic rays in the simulation.
    - SaveDetail (str): A statement used to identify the plots as for interacting or non-interacting cosmic rays when saving.
    DataMembers:
    - DistanceList (List): Contains the final verticle positions of each particle in the simulation, these are used to set the trajectory graph axis limits.

"""


def DataRead(NumberofParticles, DataFrames):
    for j in range(NumberofParticles):
        Data = pd.read_pickle('Data/Cosmic_Ray_Data_%s.csv' %(j+1))
        DataFrames.append(Data)
        DataReadPercent = round((j+1)/(NumberofParticles)*100, 1) 
        print('Data Read is %s %% complete' %(DataReadPercent))

def DataFrameShow(DataFrames):
    pd.set_option('display.max_rows', None)
    pd.options.display.max_columns = 14
    pd.options.display.width = 50000 
    Answer = str(input('Would you like to look at the data frames for any particles?\n [Type Y/N]\n')) # This loop allows the user to look at as many dataframes as they would like.
    if Answer == 'Y' or Answer == 'y':
        Repeat = 'Y'
        while Repeat == 'Y' or Repeat == "y":
            ParticleNumber = int(input('Which Particle would you like to look at?\n [Input only its number]\n'))      
            print(DataFrames[ParticleNumber-1])
            Repeat = str(input('\nWould you like to look at any more Particles?\n [Type Y/N]\n '))
        
def TrajectoryPlot(DataFrames, NumberofParticles, SaveDetail):
    DistanceList = []
    NumberInteracted = 0 
    ax = plt.axes(projection='3d')
    for i in range(len(DataFrames)): # This loop plots each cosmic ray trajectory on the same graph.
        DistanceList.append(DataFrames[i]['Y Pos [m]'][999]) # The final verticle positions of each cosmic ray are appended to the distance list.
        ax.plot3D(DataFrames[i]['X Pos [m]'], DataFrames[i]['Z Pos [m]'], DataFrames[i]['Y Pos [m]'])
        TrajectoryPercent = round((i+1)/(len(DataFrames))*100, 1) # the percentage of plots complete is calculated and printed.
        if DataFrames[i]['Interacted?'][999] == 'Yes':
            NumberInteracted += 1
        print('Data Plots are %s %% complete' %(TrajectoryPercent))
    MinYposition = min(DistanceList) # Take the minimum value from the list of final verticle values.
    MaxYposition = DataFrames[0]['Y Pos [m]'][0] # The maximum verticle position is simply the starting verticle position for any of the cosmic rays.
    difference = (MaxYposition - MinYposition)/2 # The difference is taken and used as the limits in for the X and Z axis'.
    if SaveDetail == 'Interacting': # Only runs if particles are able to interact.
        print('Mean Interaction Distance = %s m.' %(round(8E4-((sum(DistanceList))/(len(DistanceList))), 0))) # Print the mean interaction distance.
        print('%s of %s Cosmic Rays interacted.' %(NumberInteracted, NumberofParticles)) # Print the number of particles which interacted.
    
    ax.set_xlim3d(-difference, difference)
    ax.set_ylim3d(-difference, difference)
    ax.set_zlim3d(MinYposition, MaxYposition) # this is Y data, it is put on the Z axis to show cosmic rays falling downwards.
    ax.set_xlabel('X Position [m]')
    ax.set_ylabel('Z Position [m]')
    ax.set_zlabel('Y Position [m]')
    plt.savefig('Figures/Trajectory_Plot_%s_%s_Cosmic_Rays.png'%(NumberofParticles, SaveDetail),bbox_inches = 'tight') # The plot is saved into the figures folder.
    plt.show()

def DecelerationPlot(DataFrames, NumberofParticles, SaveDetail):
    for i in range(len(DataFrames)):
        plt.plot(DataFrames[i]['Time [s]'], - DataFrames[i]['Y Vel [m/s]'])
    plt.xlabel('Time [s]')
    plt.ylabel('Vertical Speed [m/s]')
    plt.savefig('Figures/Deceleration_Plot_%s_%s_Cosmic_Rays.png'%(NumberofParticles, SaveDetail),bbox_inches = 'tight') # The plot is saved into the figures folder.
    plt.show()


def EnergyLossPlot(DataFrames, NumberofParticles, SaveDetail):
    for i in range(len(DataFrames)):
        EnergyLoss = []
        for j in range(len(DataFrames[0]['Y Energy [J]'])-1):
            loss = DataFrames[i]['Y Energy [J]'][j] - DataFrames[i]['Y Energy [J]'][j+1]
            EnergyLoss.append(loss)
        EnergyLoss.append(0)
        plt.plot(-DataFrames[i]['Y Pos [m]'],  EnergyLoss)
    plt.xlabel('Vertical Distance Travelled [m]')
    plt.ylabel('Vertical Kinetic Energy transferred to Atmosphere [J]')
    plt.savefig('Figures/EnergyLoss_Plot_%s_%s_Cosmic_Rays.png'%(NumberofParticles, SaveDetail),bbox_inches = 'tight') # The plot is saved into the figures folder.
    plt.show()