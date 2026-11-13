import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from parameters import stefan_boltzmann, average_earth_radius, average_sun_radius, earth_sun_distance, c, sun_temperature, standard_earth_temp
from functions import planck_spectrum, schwarzschild_equation2, cross_section, pressure_atm, temperature_atm
import pandas as pd
from pathlib import Path
from scipy.integrate import simpson
import time
start_time = time.time()



# Calculating incoming radiation using E490 data - maybe we should change this because it doesnt account for atmospheric absorption
e490_data = pd.read_csv(
    Path(__file__).with_name("e490_data.txt"),
    sep=r'\s+',
    header=None
)
df_e490 = pd.DataFrame(e490_data)
wavelength = np.array(df_e490[df_e490.columns[0]].values.tolist()) *10**(-6) # in m
intensity_per_wavelength = np.array(df_e490[df_e490.columns[1]].values.tolist()) *10**6 # in W/m^2/m
sun_intensity = simpson(intensity_per_wavelength, wavelength)
sun_power = sun_intensity * np.pi * (average_earth_radius)**2



# Make an array for cross sections for all frequencies at all alitudes
    #parameters i could experiment with:
max_altitude = 31000 # top of atmosphere is 32km apparently
no_altitude_steps = 3

altitudes = np.linspace(0, max_altitude, no_altitude_steps)
dz = max_altitude/no_altitude_steps

HITRAN_data = pd.read_csv(
    Path(__file__).with_name("CO2Min.csv"),
    usecols=[0, 1, 2],
    header=0,
)
df_HITRAN = pd.DataFrame(HITRAN_data)
df_HITRAN_filtered = df_HITRAN[(df_HITRAN.iloc[:, 1] > 10**(-24))] # filtering out data that wont have much of an effect to make code faster
wavenumber = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[0]].values.tolist()) * 10**2 # converts to /m
absorption_frequencies = wavenumber*(c) # converts wavenumber in /m to frequency in Hz
spectral_line_intensity = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[1]].values.tolist()) * (10**(-2)) #converting units from whatever cursed units HITRAN is using to SI units
pressure_broadening = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[2]].values.tolist()) * (10**(2)) #converting units from whatever cursed units HITRAN is using to SI units
print(len(df_HITRAN.iloc[:,1])/len(wavenumber)) # this is how much is filtered out

length_of_HITRAN_filtered = len(absorption_frequencies)
cross_section_matrix = np.zeros((length_of_HITRAN_filtered, no_altitude_steps))
for alt in range(no_altitude_steps): # for each altitude step
    for r in range(length_of_HITRAN_filtered):
        for i in range(length_of_HITRAN_filtered):
            cross_section_matrix[r, alt] += cross_section(i, wavenumber[r], altitudes[alt], spectral_line_intensity, wavenumber, pressure_broadening)
print(cross_section_matrix)
print(cross_section_matrix.shape)
print(cross_section_matrix[1073,:])

if cross_section_matrix[1073, 0] == cross_section_matrix[1073, 1]:
    print('poo')
else:
    print('wee')

"""cross_section_matrix = np.zeros((1, no_altitude_steps))
for alt in range(no_altitude_steps): # for each altitude step
        for i in range(length_of_HITRAN_filtered):
            cross_section_matrix[] += cross_section(i, wavenumber[r], altitudes[alt], spectral_line_intensity, wavenumber, pressure_broadening)
print(cross_section_matrix)"""

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")