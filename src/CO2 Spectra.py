from functions import number_density
from parameters import boltzmann
import numpy as np
import pandas as pd
from pathlib import Path
from parameters import c
import matplotlib.pyplot as plt


HITRAN_data = pd.read_csv(
    Path(__file__).with_name("CO2Min.csv"),
    usecols=[0, 1, 2],
    header=0,
)
df_HITRAN = pd.DataFrame(HITRAN_data)
df_HITRAN_filtered = df_HITRAN[(df_HITRAN.iloc[:, 1] > 10**(-22))] # filtering out data that wont have much of an effect to make code faster

wavenumber = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[0]].values.tolist())
absorption_frequencies = wavenumber*(c*10**2) # converts wavenumber in /cm to frequency in Hz
spectral_line_intensity = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[1]].values.tolist()) * (10**(-2)) #converting units from whatever cursed units HITRAN is using to SI units
pressure_broadening = np.array(df_HITRAN_filtered[df_HITRAN_filtered.columns[2]].values.tolist()) * (10**(2)/101325) #converting units from whatever cursed units HITRAN is using to SI units
print(len(df_HITRAN.iloc[:,1])/len(wavenumber))

"""plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
ax.plot(
        absorption_frequencies,
        spectral_line_intensity,
        linewidth=2,
        marker="o",
        markersize=5,
        markerfacecolor="white",
        markeredgewidth=1.5,
        )
ax.set_xlabel("Frequency (Hz)", fontsize=16, fontweight="bold")
ax.set_ylabel("Spectral Line Intensity (cm/molecule)", fontsize=16, fontweight="bold")
ax.tick_params(axis="both", which="major", labelsize=14, direction="in", length=6, width=1.2)
ax.tick_params(axis="both", which="minor", direction="in", length=3, width=1)
ax.minorticks_on()
ax.grid(True, which="major", linestyle="--", alpha=0.5)
plt.show()"""

def cross_section(index, frequency, altitude):
    temperature = 296
    pressure = 101325
    """broadening_at_alt = (number_density(altitude)/(pressure/(boltzmann*temperature)))*pressure_broadening[index]"""    # we are adjusting the pressure broadening
    broadening_at_alt = pressure_broadening[index]
    return (spectral_line_intensity[index] * broadening_at_alt) / (np.pi * (broadening_at_alt**2 + (frequency - absorption_frequencies[index])**2))

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

length_ = len(absorption_frequencies)
cross_sections = np.zeros(length_)
for r in range(length_):
    for i in range(length_):
        cross_sections[r] += cross_section(i, absorption_frequencies[r], 0)

ax.scatter(
        absorption_frequencies,
        cross_sections,
        s=1
        )
ax.set_xlabel("Frequency (Hz)", fontsize=16, fontweight="bold")
ax.set_ylabel("Cross-Section (/cm^2)", fontsize=16, fontweight="bold")
ax.tick_params(axis="both", which="major", labelsize=14, direction="in", length=6, width=1.2)
ax.tick_params(axis="both", which="minor", direction="in", length=3, width=1)
ax.minorticks_on()
ax.grid(True, which="major", linestyle="--", alpha=0.5)
plt.show()