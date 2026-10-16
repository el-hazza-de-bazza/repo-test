from functions import planck_spectrum
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

temps = np.arange(100, 1001, 100)
freq_range = np.linspace(10**12, 10**20, 10)

# Plotting with publication-ready styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

for i in temps:
    ax.plot(
        freq_range,
        planck_spectrum(freq_range, temps[i]),
        #color="#d62728",      # Elegant crimson red
        linewidth=2,
        marker="o",
        markersize=5,
        markerfacecolor="white",
        markeredgewidth=1.5,
        label="FIX ME"
        )


# Axis labels and limits
ax.set_xlabel("Frequency (Hz)", fontsize=16, fontweight="bold")
ax.set_ylabel("Spectral Radiance (bs)", fontsize=16, fontweight="bold")
#ax.set_xlim(1.6, )

# Styling ticks & grid
ax.tick_params(axis="both", which="major", labelsize=14, direction="in", length=6, width=1.2)
ax.tick_params(axis="both", which="minor", direction="in", length=3, width=1)
ax.minorticks_on()
ax.grid(True, which="major", linestyle="--", alpha=0.5)

# Annotations & Title
ax.set_title("Planck Spectrum Test", fontsize=20, pad=12, fontweight="bold")
ax.legend(frameon=True, facecolor="white", edgecolor="none", fontsize=14, loc="best")

plt.tight_layout()
plt.savefig("Planck Spectrum Test.png", dpi=300)
plt.show()