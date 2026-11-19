import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from parameters import average_earth_radius ,g, co2_concentration, stefan_boltzmann, boltzmann, average_earth_radius, average_sun_radius, earth_sun_distance, c, sun_temperature, standard_earth_temp, average_albedo, standard_earth_pressure
from functions import planck_spectrum, schwarzschild_equation2, cross_section, pressure_atm, temperature_atm, spectral_irradiance
import pandas as pd
from pathlib import Path
from scipy.integrate import simpson
import math
import time
start_time = time.time()

#PARAMETERS
max_altitude = 32000 # these two parameters dont matter anymore with our new single layer model
no_altitude_steps = 1
albedo = average_albedo
CO2_ppm = 430 * 10 ** (-6) # 430ppm is current
atm_pressure = standard_earth_pressure
average_mass_air_molecule = 4.81 * 10**(-26)



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
sun_power = (1-albedo) * sun_intensity * np.pi * (average_earth_radius)**2

"""modtran_csv = Path(__file__).with_name("modtran_radiance.csv")
modtran_frequency_hz = np.array([])
modtran_radiance = np.array([])
if modtran_csv.exists():
    modtran_df = pd.read_csv(modtran_csv)
    if {"frequency_hz", "total_radiance_W_m2_sr_Hz"}.issubset(modtran_df.columns):
        modtran_frequency_hz = modtran_df["frequency_hz"].to_numpy(dtype=float)
        modtran_radiance = modtran_df["total_radiance_W_m2_sr_Hz"].to_numpy(dtype=float)"""



# Make an array for cross sections for all frequencies at all alitudes
    #parameters i could experiment with:


"""altitudes = np.linspace(0, max_altitude, no_altitude_steps)
dz = max_altitude/no_altitude_steps"""

HITRAN_data = pd.read_csv(
    Path(__file__).with_name("CO2_wider.csv"),
    usecols=[0, 1, 2],
    header=0,
)
df_HITRAN = pd.DataFrame(HITRAN_data)
df_HITRAN_filtered = df_HITRAN[(df_HITRAN.iloc[:, 1] > 10**(-35))] # filtering out data that wont have much of an effect to make code faster
wavenumber = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[0]].values.tolist()) * 10**2 # converts to /m
absorption_frequencies = wavenumber*(c) # converts wavenumber in /m to frequency in Hz
spectral_line_intensity = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[1]].values.tolist()) * (10**(-2)) #converting units from whatever cursed units HITRAN is using to SI units
pressure_broadening = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[2]].values.tolist()) * (10**(2)) #converting units from whatever cursed units HITRAN is using to SI units
print(len(df_HITRAN.iloc[:,1])/len(wavenumber)) # this is how much is filtered out
length_of_HITRAN_filtered = len(absorption_frequencies)

# cross section stuff
cross_section_matrix = np.zeros(length_of_HITRAN_filtered)
"""for alt in range(no_altitude_steps): # for each altitude step"""
for r in range(length_of_HITRAN_filtered):
    for i in range(length_of_HITRAN_filtered):
        cross_section_matrix[r] += cross_section(i, wavenumber[r], spectral_line_intensity, wavenumber, pressure_broadening)
print('cross sections calculated')

#parameters for loop:
tolerance = 10**10
error = tolerance * 10
trial_temps = np.array([200, 400], dtype = 'float')
freq_step_size = 10**12
min_freq = 10**11
max_freq = 10**14

total_earth_power_trial = np.array([0, 0])
for k in range(len(trial_temps)):
    earth_temp = trial_temps[k]
    length_of_HITRAN_filtered = length_of_HITRAN_filtered
    spectral_radiance_array = np.empty(length_of_HITRAN_filtered)
    z_0 = (boltzmann * earth_temp) / (g * average_mass_air_molecule)
    trop_temp = earth_temp + 0.00649 * z_0 * math.log((1 - 0.75), 10)
    atm_temp = earth_temp # yep this is a poor model assuming isothermal
    atm_number_density_CO2 = CO2_ppm * atm_pressure/(boltzmann*atm_temp)
    for i in range(length_of_HITRAN_filtered):
        optical_depth = atm_number_density_CO2 * cross_section_matrix[i] * z_0
        exp_optical_depth = np.exp( -1 * optical_depth)
        spectral_radiance_array[i] = (planck_spectrum(absorption_frequencies[i], earth_temp)*exp_optical_depth ) + ( planck_spectrum(absorption_frequencies[i], trop_temp) * (1 - exp_optical_depth))
    spectral_irradiance_array = 4 * (np.pi**2) * ((average_earth_radius+max_altitude)**2) * spectral_radiance_array # power per frequency becuase we integrate over solid angle and mutliply by surface area of sphere
    #Integrate over frequency:
    earth_power_co2 = simpson(spectral_irradiance_array, absorption_frequencies)
    
    # integrate other parts of earth spectrum: replace this with actual data at some point?
    frequencies_section_1 = np.arange(min_freq, absorption_frequencies[0], freq_step_size)
    SI_1 = np.zeros(len(frequencies_section_1))
    for i in range(len(frequencies_section_1)):
        SI_1[i] = spectral_irradiance(average_earth_radius, max_altitude + average_earth_radius, frequencies_section_1[i], earth_temp)
    earth_power_1 = simpson(4 * (np.pi) * ((average_earth_radius+max_altitude)**2) * SI_1, frequencies_section_1)
    frequencies_section_3 = np.arange(absorption_frequencies[-1], max_freq, freq_step_size)
    SI_3 = np.zeros(len(frequencies_section_3))
    for i in range(len(frequencies_section_3)):
        SI_3[i] = spectral_irradiance(average_earth_radius, max_altitude + average_earth_radius, frequencies_section_3[i], earth_temp)
    earth_power_3 = simpson(4 * (np.pi) * ((average_earth_radius+max_altitude)**2) * SI_3, frequencies_section_3) 
    
    total_earth_power_trial[k] = earth_power_1 + earth_power_co2 + earth_power_3
    print(f"{k+1} trial calculated")

assert total_earth_power_trial[0] < sun_power
assert total_earth_power_trial[1] > sun_power
iteration = 0

while abs(error) > tolerance:
    # schwarschild time!!
    # just doing single layer
    earth_temp = (trial_temps[0] + trial_temps[1]) / 2
    length_of_HITRAN_filtered = length_of_HITRAN_filtered
    spectral_radiance_array = np.empty(length_of_HITRAN_filtered)
    z_0 = (boltzmann * earth_temp) / (g * average_mass_air_molecule)
    trop_temp = earth_temp + 0.00649 * z_0 * math.log((1 - 0.75), 10)
    atm_temp = earth_temp # yep this is a poor model assuming isothermal
    atm_number_density_CO2 = CO2_ppm * atm_pressure/(boltzmann*atm_temp)
    for i in range(length_of_HITRAN_filtered):
        optical_depth = atm_number_density_CO2 * cross_section_matrix[i] * z_0
        exp_optical_depth = np.exp( -1 * optical_depth)
        spectral_radiance_array[i] = (planck_spectrum(absorption_frequencies[i], earth_temp)*exp_optical_depth ) + ( planck_spectrum(absorption_frequencies[i], trop_temp) * (1 - exp_optical_depth))
    spectral_irradiance_array = 4 * (np.pi**2) * ((average_earth_radius+max_altitude)**2) * spectral_radiance_array # power per frequency becuase we integrate over solid angle and mutliply by surface area of sphere
    #Integrate over frequency:
    earth_power_co2 = simpson(spectral_irradiance_array, absorption_frequencies)

    # integrate other parts of earth spectrum: replace this with actual data at some point?
    frequencies_section_1 = np.arange(min_freq, absorption_frequencies[0], freq_step_size)
    SI_1 = np.zeros(len(frequencies_section_1))
    for i in range(len(frequencies_section_1)):
        SI_1[i] = spectral_irradiance(average_earth_radius, max_altitude + average_earth_radius, frequencies_section_1[i], earth_temp)
    earth_power_1 = simpson(4 * (np.pi) * ((average_earth_radius+max_altitude)**2) * SI_1, frequencies_section_1) 
    frequencies_section_3 = np.arange(absorption_frequencies[-1], max_freq, freq_step_size)
    SI_3 = np.zeros(len(frequencies_section_3))
    for i in range(len(frequencies_section_3)):
        SI_3[i] = spectral_irradiance(average_earth_radius, max_altitude + average_earth_radius, frequencies_section_3[i], earth_temp)
    earth_power_3 = simpson(4 * (np.pi) * ((average_earth_radius+max_altitude)**2) * SI_3, frequencies_section_3) 

    total_earth_power = earth_power_1 + earth_power_co2 + earth_power_3
    if total_earth_power < sun_power:
        trial_temps[0] = earth_temp
    if total_earth_power > sun_power:
        trial_temps[1] = earth_temp
    error = total_earth_power - sun_power
    iteration += 1
    print(f"{iteration} iteration calculated with temperature {earth_temp} K")

print(total_earth_power)
print(sun_power)
print(earth_temp)


end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

#plot this bad boy
import matplotlib as mpl
import matplotlib.font_manager
from IPython.core.display import HTML
mpl.rcParams['font.family'] = 'cmr10'
fig, ax = plt.subplots(figsize=(8, 4), dpi=150)

spectral_irradiance_array = spectral_irradiance_array / (4 * (np.pi) * ((average_earth_radius+max_altitude)**2)) # for power density, remove the division by (4 * (np.pi) * ((average_earth_radius+max_altitude)**2))
power_per_freq_1 = SI_1 # for power density, multiple by (4 * (np.pi) * ((average_earth_radius+max_altitude)**2))
power_per_freq_3 = SI_3 # for power density, multiple by (4 * (np.pi) * ((average_earth_radius+max_altitude)**2))
power_per_freq = np.append(power_per_freq_1, spectral_irradiance_array)
power_per_freq = np.append(power_per_freq, power_per_freq_3)
freq_sections = np.append(frequencies_section_1, absorption_frequencies)
freq_sections = np.append(freq_sections, frequencies_section_3)
ax.plot(freq_sections*10**(-12), power_per_freq*10**(12), color = "#1F289C", label='430ppm')

"""if modtran_frequency_hz.size > 0 and modtran_radiance.size > 0:
    modtran_order = np.argsort(modtran_frequency_hz)
    ax.plot(
        modtran_frequency_hz[modtran_order],
        4 * (np.pi**2) * ((average_earth_radius+max_altitude)**2) * modtran_radiance[modtran_order],
        color='black',
        linestyle='--',
        linewidth=1.5,
        label='MODTRAN simulation'
    )"""

ax.set_xlabel("Frequency (THz)", fontsize=18, fontweight="bold")
ax.set_ylabel("Spectral Irradiance\n(10$^{-12}$ Wm$^{-2}$Hz$^{-1}$)", fontsize=18, fontweight="bold")
ax.tick_params(axis="both", which="major", labelsize=14, direction="in", length=6, width=1.2)
ax.tick_params(axis="both", which="minor", direction="in", length=3, width=1)
ax.minorticks_on()
#ax.grid(True, which="major", linestyle="--", alpha=0.5)
ax.legend(fontsize=16, facecolor = "#1F289C", framealpha = 0)
ax.set_xlim(-1.5, 61)
fig.tight_layout()

"""# The MODTRAN output spans many orders of magnitude, so a log scale keeps the comparison readable.
if modtran_frequency_hz.size > 0 and modtran_radiance.size > 0:
    ax.set_yscale('log')"""

plt.savefig("earth_spectral_irradiance.png", dpi=150)
plt.show()

