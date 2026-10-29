import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from parameters import stefan_boltzmann, average_earth_radius, average_sun_radius, earth_sun_distance, c, sun_temperature
from functions import planck_spectrum
import pandas as pd
from pathlib import Path
from scipy.integrate import simpson

e490_data = pd.read_csv(
    Path(__file__).with_name("e490_data.txt"),
    sep=r'\s+',
    header=None
)
df_e490 = pd.DataFrame(e490_data)
wavelength = np.array(df_e490[df_e490.columns[0]].values.tolist()) *10**(-6) # in m
intensity_per_wavelength = np.array(df_e490[df_e490.columns[1]].values.tolist()) *10**6 # in W/m^2/m

sun_intensity_e490 = simpson(intensity_per_wavelength, wavelength)
sun_intensity_planck = (stefan_boltzmann * (5772)**4) * (average_sun_radius/earth_sun_distance)**2
albedo = 0.3
T_earth_planck = (((np.pi * (average_earth_radius**2)) * sun_intensity_planck * (1 - albedo)) / (stefan_boltzmann * (4 * np.pi * (average_earth_radius**2))))**(1/4)
T_earth_e490 = (((np.pi * (average_earth_radius**2)) * sun_intensity_e490 * (1 - albedo)) / (stefan_boltzmann * (4 * np.pi * (average_earth_radius**2))))**(1/4)
print(T_earth_planck)
print(sun_intensity_planck)
print(T_earth_e490)
print(sun_intensity_e490)

planck_intensity = np.pi * ((average_sun_radius/earth_sun_distance)**2) * planck_spectrum(c/wavelength, sun_temperature) * (c / (wavelength**2))
#plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
import matplotlib as mpl
import matplotlib.font_manager
from IPython.core.display import HTML
dpi = 150 
mpl.rcParams['font.family'] = 'cmr10'
fig, ax = plt.subplots(figsize=(8, 4), dpi=dpi)

frequency_THz = c / wavelength / 1e12
intensity_per_frequency = intensity_per_wavelength * wavelength**2 / c
planck_per_frequency = planck_intensity * wavelength**2 / c

# Frequency decreases as wavelength increases; sort so the plot runs left to right.
order = np.argsort(frequency_THz)

ax.plot(frequency_THz[order], planck_per_frequency[order]*10**(12), color = "#1F289C", linewidth = 5, label = "Predicted Solar Radiation")
ax.plot(frequency_THz[order], intensity_per_frequency[order]*10**(12), color = "#1f73e0", linewidth = 1.5, label = "E490 Data")
ax.set_xlim(0, 1500)
ax.set_ylim(0, 2.65)
ax.set_xlabel("Frequency (THz)", fontsize=18, fontweight="bold")
ax.set_ylabel("Spectral Irradiance\n(10$^{-12}$ W m$^{-2}$ Hz$^{-1}$)", fontsize=18, fontweight="bold")

"""ax.plot(
        wavelength,
        intensity_per_wavelength
        )
ax.plot(
        wavelength,
        planck_intensity
        )
ax.set_xlim(0, 4*10**-6)
ax.set_xlabel("Wavelength (m)", fontsize=16, fontweight="bold")
ax.set_ylabel("intensity sort of????????????", fontsize=16, fontweight="bold")"""
ax.tick_params(axis="both", which="major", labelsize=14, direction="in", length=6, width=1.2)
ax.tick_params(axis="both", which="minor", direction="in", length=3, width=1)
ax.minorticks_on()
ax.legend(fontsize = 16)
#ax.grid(True, which="major", linestyle="--", alpha=0.5)
fig.tight_layout()
plt.savefig("solar radiation intensity2.png", dpi=dpi)
plt.show()

"""#plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
import matplotlib as mpl
import matplotlib.font_manager
from IPython.core.display import HTML
mpl.rcParams['font.family'] = 'cmr10'
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)


length_ = len(absorption_frequencies)
cross_sections = np.zeros(length_)
for r in range(length_):
    for i in range(length_):
        cross_sections[r] += cross_section(i, wavenumber[r], 0)

ax.plot(
        wavenumber*c*10**(-12),
        cross_sections
        
        )
ax.set_xlabel("Frequency (THz)", fontsize=18, fontweight="bold")
ax.set_ylabel("Cross-Section (m$^{-2}$)", fontsize=18, fontweight="bold")
ax.tick_params(axis="both", which="major", labelsize=14, direction="in", length=6, width=1.2)
ax.tick_params(axis="both", which="minor", direction="in", length=3, width=1)
ax.minorticks_on()
ax.set_yscale('log')
#ax.grid(True, which="major", linestyle="--", alpha=0.5)
plt.savefig("co2 cross section v1.png", dpi=150)
plt.show()"""