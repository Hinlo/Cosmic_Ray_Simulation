Simulating Cosmic Rays Entering Earth's Atmosphere ~ Finlo Heath
This text file describes how to run the python simulation built for PHYS 389 Computer Modelling.
There are eight python files and two folders, included in the same folder as this README, required 
to run the simulation:


RunSimilation.py
(User Action Required)

Imports Atmosphere from AtmosphereFinal.py. Imports DataRead, DataFrameShow, TrajectoryPlot, 
DecelerationPlot and EnergyLossPlot functions from RunSimulationSupportFunctions.py.
This is the only file which requires user interaction. It should be run in the terminal and when run
requires two user inputs when run: 
 - The number of cosmic rays in the simulation (a sensible choice would be between 1-1000).
 - Whether or not the cosmic rays will be able to interact. 
Once these have been input, the file runs the Atmosphere function which simulates each cosmic ray in
sequence. As the cosmic rays do not interact in this simulation, they can be run consecutively rather
than all at once. The DataRead function reads the files created in the simulation. The DataFrameShow
function provides the user the opportunity to look at the dataframes of any of the cosmic rays via user
input in the terminal. The final three functions that are run create plots of the data. The plots 
include a trajectory plot, a plot of vertical velocity over time and a plot of energy loss over 
time. These are displayed when the file is run and saved.
- The dataframes are saved in the Data folder. These are overwritten with each simulation to avoid 
accumulating too many files.
- The plots are saved in the Figures folder. These are overwritten with each simulation to avoid 
accumulating too many files. 
Since interacting simulations will produce different data each simulation, the user should consider
copying images from the figures folder to a separate folder before running the next simulation. 
Non-interacting simulations will produce the same data each time.


Particle.py
(No User Action Required)

Imports no functions.
Contains two classes. No adjustments need to be made by the user to this file.
Particle is a class which creates a neutral, non-relativistic massive particles
and provides functions to measure that particles kinetic energy, momentum and beta value as well as 
to update the particles position and velocity values. It returns a statement with the current
parameters of the particle.
Charticle is a class which inherits a Particle and gives it a charge parameter relative to the 
electron charge magnitude. It returns a statement with the current parameters of the particle. 
 

CosmicRayClass.py
(No User Action Required)

Imports Charticle Class from Particle.py. Imports StoppingForce, NonRelativisticStoppingForce and
ForceDirectionCheck from CosmicRaySupportFunctions.py.
No adjustments need to be made by the user to this file.
Contains the CosmicRay class which inherits a Charticle and gives it three more parameters; RestMass,
Interact and Gamma. These are used in the class functions. The CosmicRayUpdate function updates the
spatial parameters of the cosmic ray for a given time step. The StoppingForce and NonRelativisticSto-
ppingForce functions called in this function are set for the parameters of the mesosphere (the first a-
tmospheric layer where air density is not negligible) as cosmic rays stop before roughly the lower limit
of the mesosphere and are initialised at the upper limit of the mesosphere. The interactionCheck function 
calculates a value for whether the particle interacts each time step or passes if the cosmic ray has 
interacted already. The GammaUpdate function updates the lorentz factor value attributed to the cosmic 
ray. The MassUpdate function uses the Lorentz factor value to update the cosmic ray's mass due to 
relativistic speeds. The ParticleEnergyUpdate function uses the relativistic mass to update the total 
energy of the particle. 


CosmicRaySupportFunctions
(No User Action Required)

Imports no functions.
Contains three functions. No adjustments need to be made by the user to this file.
The StoppingForce and NonRelativisticStoppingForce functions calculate the electronic stopping force 
acting on moving relativistic and non-relativistic cosmic rays respectively. The ForceDirectionCheck
checks and ensures that the stopping force always acts to oppose the motion of the cosmic ray.


AtmosphereFinal.py
(No User Action Required)

Imports CosmicRay class from CosmicRayClass.py. Imports BunchFunction, Direction and Interacted 
functions from AtmosphereSupportFunctions.py. No adjustments need to be made by the user to this file.
Contains the Atmosphere function. This function runs the simulation for a given number of cosmic rays, 
over a given run time and with particle interactions set be to on or off. Dataframes are produced for
each cosmic ray which are saved in the Data folder as specified above.
  

AtmosphereSupportFunctions.py
(No User Action Required)

Imports CosmicRay class from CosmicRayClass.py. User may edit this file to adjust the 
initial parameters of each cosmic ray.
Contains Three Functions. The BunchFunction function creates a list of the cosmic rays to be used in 
the simulation and sets their initial parameters. These can be adjusted by the user if desired but are 
currently set to produce the most useful data. Initial cosmic ray position is set to the top of the 
mesosphere (the first atmospheric layer where air density is not negligible). Cosmic ray velocities 
are set so that their velocity magnitude of each cosmic ray in the bunch increases from 0.43c to 
roughly 0.996c which are the upper and lower limits of observed cosmic ray velocities. This ensures 
that each simulation displays the full range of possible cosmic ray velocities. The velocities are 
also set such that the direction of each cosmic ray in the x-z plane is unique so that each can be
observed on the trajectory plot of the simulation. The cosmic rays are set to be protons (have proton
mass and charge of +1 relative to the electron charge magnitude).
The Direction function generates a list which represents the direction of the components of the cosmic
ray's initial velocity vector. This is used to ensure the cosmic ray does not begin to accelerated in 
the opposite direction once it has slowed down and stopped. The Interacted function checks whether the
cosmic ray has interacted and returns a statement of 'Yes' or 'No'. 


RunSimulationSupportFunctions.py
(No User Action Required)

Imports no functions. No adjustments need to be made by the user to this file. 
Contains five Functions. The DataRead function reads the data files in the Data folder and appends them
to a single list. The DataframeShow function is a user input loop that allows the user to view any of 
the cosmic ray dataframes from the simulation. The TrajectoryPlot function is a 3D plot displaying the
trajectory of each cosmic ray in the simulation. The DecelerationPlot function is a plot of the 
vertical velocity of each cosmic ray over the run time. The EnergyLossPlot function is a plot of the 
total energy of each cosmic ray over the run time of the simulation.

test_CosmicRay.py
(No User Action Required)

Imports CosmicRay class from CosmicRayClass.py. Imports the Bunchfunction, Direction and Interacted
functions from AtmosphereSupportFunctions.py. Imports StoppingForce, NonRelativisticStoppingForce and
ForceDirectionCheck from CosmicRaySupportFunctions.py. 
User may edit this file to adjust the parameters of each test.
This file contains test functions for each of the functions imported as well as for each of the testable
functions in the CosmicRayClass. The functions for which test files are not written are those such as 
functions which generate plots which do not have any obvious outcomes for which to test.
If changes to the simulation parameters are made the user will need to update the test functions with 
the new expected results corresponding to these changes.

Data Folder
Pickled dataframes are saved here. They will be overwritten with each simulation. Therefore Users should 
copy any important dataframes to a separate folder.

Figures Folder
Plots are saved here. They will be overwritten with each simulation. Therefore Users should 
copy any important figures to a separate folder. 