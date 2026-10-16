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
plt.subplots_adjust(bottom=0.25)

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

initial_temp = 800
initial_max_freq = 2*10**14
special_freq_range = np.linspace(10**12, initial_max_freq, 50)
curve, = ax.plot(special_freq_range,
        planck_spectrum(special_freq_range, initial_temp),
        color='black',      # Elegant crimson red
        linewidth=2,
        marker="o",
        markersize=5,
        markerfacecolor="white",
        markeredgewidth=1.5,
        )
#line, = ax.axvline(5.87892576 * 10**10 * initial_temp, color='black', linestyle='-', linewidth=1)

ax_slider1 = fig.add_axes([0.25, 0.1, 0.65, 0.03])
temp_slider = Slider(
    ax=ax_slider1,
    label='Temperature',
    valmin=100,
    valmax=10000,
    valinit=initial_temp,
)
ax_slider2 = fig.add_axes([0.25, 0.05, 0.65, 0.03])
maximum_freq_slider = Slider(
    ax=ax_slider2,
    label='Maximum Frequency',
    valmin=2*10**14,
    valmax=2*10**15,
    valinit=2*10**14,
)

# 3. Define the update function
def update(val):
    current_temp = temp_slider.val
    current_max_freq = maximum_freq_slider.val
    current_freq_range = np.linspace(10**12, current_max_freq, 50)
    curve.set_ydata(planck_spectrum(current_freq_range, current_temp))
    curve.set_xdata(current_freq_range)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()  # Redraw the figure efficiently

# 4. Connect the slider to the update function
temp_slider.on_changed(update)
maximum_freq_slider.on_changed(update)

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