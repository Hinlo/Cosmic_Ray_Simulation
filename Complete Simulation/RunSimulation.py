import numpy as np
import pandas as pd
import math
import copy
import random
from scipy import constants
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from RunSimulationSupportFunctions import DataRead, DataFrameShow, TrajectoryPlot, DecelerationPlot, EnergyLossPlot
from AtmosphereFinal import Atmosphere
""" 
This is the only file that the user needs to run in the terminal.
Runs cosmic ray simulation using the Atmosphere Function in the AtmosphereFinal file as well as supporting functions in the RunSimulationSupportFunctions file.

Parameters:
- Parameters for the Atmosphere function are specified in this file. See the AtmosphereFinal file for parameter details.


Data Members:
- NumberofParticles (int, User Input): The number of cosmic rays the user would like to simulate.
- InteractionOnOff (str, User Input): A statement to select whether the user would like particles to have the ability to interact with atmospheric particles or not.
"""

NumberofParticles = int(input('How many Cosmic Rays would you like?\n')) 
InteractionOnOff = str(input('Would you like: \n - Non-Interacting Primary Cosmic Rays? [Input N] \n - Interacting Cosmic Rays [Input I] \n'))
if InteractionOnOff == 'I' or InteractionOnOff == 'i':
    SaveDetail = 'Interacting'
else:
    SaveDetail = 'Non_Interacting'
dataframelist = []

Atmosphere(0.000184, NumberofParticles, InteractionOnOff) # Run the simulation.
DataRead(NumberofParticles,dataframelist) # Read the data files created in the simulation.
DataFrameShow(dataframelist) # Provides the option to print dataframes the user is interested in.
TrajectoryPlot(dataframelist, NumberofParticles, SaveDetail) # Create a plot of the trajectory of the cosmic rays.
DecelerationPlot(dataframelist, NumberofParticles, SaveDetail) # Create a plot of the verticle deceleration of the cosmic rays over time.
EnergyLossPlot(dataframelist, NumberofParticles, SaveDetail) # Create a plot of the total energy loss of the cosmic rays over time.


