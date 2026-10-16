from functions import planck_spectrum
from parameters import c
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd
import numpy as np

temps = np.arange(300, 1001, 150)
freq_range = np.linspace(10**12, 2*10**14, 50)

# Plotting with publication-ready styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

rainbow_colors = [
    '#FF0000',  # 1. Pure Red
    #'#FF3300',  # 2. Red-Orange
    '#FF6600',  # 3. Orange
    #'#FF9900',  # 4. Amber-Orange
    '#FFCC00',  # 5. Yellow-Orange
    #'#FFFF00',  # 6. Pure Yellow
    #'#99CC00',  # 7. Yellow-Green
    #'#33CC00',  # 8. Lime Green
    '#00CC66',  # 9. Green
    #'#00CCCC',  # 10. Turquoise / Cyan-Green
    #'#0099FF',  # 11. Cyan / Light Blue
    '#0066FF',  # 12. Dodger Blue
    #'#0033FF',  # 13. Blue
    #'#0000FF',  # 14. Deep Blue
    #'#0000CC'   # 15. Dark Indigo/Blue
]

for i in range(len(temps)):
    ax.plot(
        freq_range,
        planck_spectrum(freq_range, temps[i]),
        color=rainbow_colors[-i-1],      # Elegant crimson red
        linewidth=2,
        marker="o",
        markersize=5,
        markerfacecolor="white",
        markeredgewidth=1.5,
        label=temps[i]
        )
    ax.axvline(5.87892576 * 10**10 * temps[i], color=rainbow_colors[-i-1], linestyle='--', linewidth=1)


# Axis labels and limits
ax.set_xlabel("Frequency (Hz)", fontsize=16, fontweight="bold")
ax.set_ylabel("Spectral Radiance (W/m2/sr/Hz)", fontsize=16, fontweight="bold")

# Styling ticks & grid
ax.tick_params(axis="both", which="major", labelsize=14, direction="in", length=6, width=1.2)
ax.tick_params(axis="both", which="minor", direction="in", length=3, width=1)
ax.minorticks_on()
ax.grid(True, which="major", linestyle="--", alpha=0.5)

# Annotations & Title
ax.set_title("Planck Spectrum Test", fontsize=20, pad=12, fontweight="bold")
ax.legend(frameon=True, facecolor="white", edgecolor="none", fontsize=14, loc="best")

#plt.tight_layout()
plt.savefig("Planck Spectrum Test.png", dpi=150)
plt.show()