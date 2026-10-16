from parameters import h
from parameters import c
from parameters import boltzmann
import math
import numpy as np
def planck_spectrum(freq, temperature):
    #accepts freq in Hz and temperature in K
    #returns spectral radiance in units W / m^2 / sr / Hz
    return (2*h*(freq**3)/(c**2))/(np.exp((h*freq)/(boltzmann*temperature)) - 1)

