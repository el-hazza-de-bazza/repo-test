from parameters import h
from parameters import c
from parameters import boltzmann
import math
import numpy as np

#Planck Radiation Law:
def planck_spectrum(freq, temperature):
    #accepts freq in Hz and temperature in K
    #returns spectral radiance in units W / m^2 / sr / Hz
    return (2*h*(freq**3)/(c**2))/(np.exp((h*freq)/(boltzmann*temperature)) - 1)

#Number density in atmosphere - derived from ideal gas law
def number_density(altitude):
    #accepts altitude above sea level
    #should take data from a source for pressure and temperature - later venture
    # currently uses sea level temperature (T=296K as used by HITRAN) and pressure (1 atm = 101325 Pa)
    temperature = 296
    pressure = 101325
    return pressure/(boltzmann*temperature)

def spectral_irradiance(radius_of_source, distance, frequency, temperature):
    return np.pi * planck_spectrum(frequency, temperature) * (radius_of_source/distance)**2