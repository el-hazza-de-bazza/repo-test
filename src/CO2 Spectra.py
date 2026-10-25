from parameters import boltzmann
import numpy as np
import pandas as pd
from pathlib import Path
from parameters import c
import matplotlib.pyplot as plt
from functions import temperature_atm, pressure_atm, number_density

HITRAN_data = pd.read_csv(
    Path(__file__).with_name("CO2Min.csv"),
    usecols=[0, 1, 2],
    header=0,
)
df_HITRAN = pd.DataFrame(HITRAN_data)
df_HITRAN_filtered = df_HITRAN[(df_HITRAN.iloc[:, 1] > 10**(-24))] # filtering out data that wont have much of an effect to make code faster

wavenumber = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[0]].values.tolist()) * 10**2 # converts to /m
absorption_frequencies = wavenumber*(c) # converts wavenumber in /cm to frequency in Hz
spectral_line_intensity = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[1]].values.tolist()) * (10**(-2)) #converting units from whatever cursed units HITRAN is using to SI units
pressure_broadening = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[2]].values.tolist()) * (10**(2)) #converting units from whatever cursed units HITRAN is using to SI units.101325
print(len(df_HITRAN.iloc[:,1])/len(wavenumber))

"""def cross_section(index, frequency, altitude):
    temperature = 296
    pressure = 101325
    broadening_at_alt = (number_density(altitude)/(pressure/(boltzmann*temperature)))*pressure_broadening[index]    # we are adjusting the pressure broadening
    broadening_at_alt = pressure_broadening[index]
    return (spectral_line_intensity[index] * broadening_at_alt) / (np.pi * (broadening_at_alt**2 + (frequency - wavenumber[index])**2))"""

def cross_section(index, frequency, altitude):
    temperature = 296 # this is correct
    pressure = 101325 # yeah leave this
    broadening_at_alt = (number_density(altitude)/(pressure/(boltzmann*temperature)))*pressure_broadening[index]    # we are adjusting the pressure broadening
    return (spectral_line_intensity[index] * broadening_at_alt) / (np.pi * (broadening_at_alt**2 + (frequency - wavenumber[index])**2))

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

length_ = len(absorption_frequencies)
cross_sections = np.zeros(length_)
for r in range(length_):
    for i in range(length_):
        cross_sections[r] += cross_section(i, wavenumber[r], 0)

ax.plot(
        wavenumber*c,
        cross_sections
        
        )
ax.set_xlabel("Wavenumber (/m)", fontsize=16, fontweight="bold")
ax.set_ylabel("Cross-Section (/m^2)", fontsize=16, fontweight="bold")
ax.tick_params(axis="both", which="major", labelsize=14, direction="in", length=6, width=1.2)
ax.tick_params(axis="both", which="minor", direction="in", length=3, width=1)
ax.minorticks_on()
ax.grid(True, which="major", linestyle="--", alpha=0.5)
plt.show()

"""from functions import spectral_irradiance
altitude = 10 # metres
radius_earth = 6.3781 * 10**6 # metres
from parameters import co2_concentration

freq_step_size = 10**12
frequencies_section_1 = np.arange(10**11, wavenumber[0]*c, freq_step_size)
SI_1 = np.zeros(len(frequencies_section_1))
frequencies_section_3 = np.arange(wavenumber[-1]*c, 10**14, freq_step_size)
SI_3 = np.zeros(len(frequencies_section_3))
frequencies_section_2 = wavenumber*c
SI_2 = np.zeros(len(frequencies_section_2))

for i in range(len(frequencies_section_1)):
    SI_1[i] = spectral_irradiance(radius_earth, altitude + radius_earth, frequencies_section_1[i], 296)
for i in range(len(frequencies_section_3)):
    SI_3[i] = spectral_irradiance(radius_earth, altitude + radius_earth, frequencies_section_3[i], 296)
for i in range(len(frequencies_section_2)):
    SI_2[i] = spectral_irradiance(radius_earth, altitude + radius_earth, frequencies_section_2[i], 296) * np.exp(-1 * altitude * co2_concentration * number_density(altitude) * cross_sections[i])

SI = np.append(SI_1, [SI_2])
SI = np.append(SI, [SI_3])
freq_sections = np.append(frequencies_section_1, [frequencies_section_2])
freq_sections = np.append(freq_sections, [frequencies_section_3])
ax.plot(freq_sections, SI, color = 'red')


ax.set_xlabel("Wavenumber (/m)", fontsize=16, fontweight="bold")
ax.set_ylabel("Cross-Section (/m^2)", fontsize=16, fontweight="bold")
ax.tick_params(axis="both", which="major", labelsize=14, direction="in", length=6, width=1.2)
ax.tick_params(axis="both", which="minor", direction="in", length=3, width=1)
ax.minorticks_on()
ax.grid(True, which="major", linestyle="--", alpha=0.5)
plt.savefig("CO2 Spectra V1.png", dpi=150)
plt.show()"""