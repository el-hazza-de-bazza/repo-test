from functions import number_density
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
wavenumber = np.array(df_HITRAN[df_HITRAN.columns[0]].values.tolist())
frequency = wavenumber*(c*10**2) # converts wavenumber in /cm to frequency in Hz
spectral_line_intensity = np.array(df_HITRAN[df_HITRAN.columns[1]].values.tolist()) * (10**(-2)) #converting units from whatever cursed units HITRAN is using to SI units
pressure_broadening = np.array(df_HITRAN[df_HITRAN.columns[2]].values.tolist()) * (10**(2)/101325) #converting units from whatever cursed units HITRAN is using to SI units

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
ax.plot(
        frequency,
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
plt.show()