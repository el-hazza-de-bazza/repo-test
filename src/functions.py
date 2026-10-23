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

# Temperature and pressure models taken from ICAO Standard Atmosphere model : https://en.wikipedia.org/wiki/International_Standard_Atmosphere and https://www.aviationhunt.com/standard-atmosphere-calculator/
#Atmospheric Temperature:
def temperature_atm(altitude):
    assert altitude >= 0
    if 11000 > altitude >= 0:
        return 273.15 + 15.0 - (6.5 * altitude/1000)
    if 20000 > altitude >= 11000:
            return 273.15 - 56.5
    if 32000 > altitude >= 20000:
            return 273.15 - 56.5 + (1 * (altitude - 20000)/1000)
    if altitude >= 32000:
            return 273.15 - 44.5

#Atmospheric pressure: based off ICAO Standard Atmosphere https://www.aviationhunt.com/standard-atmosphere-calculator/ and https://wiki.ivao.aero/en/home/training/documentation/International_standard_atmosphere_ISA
def pressure_atm(altitude):
    assert altitude >= 0
    if 11000 > altitude >= 0:
        return 101325 * (temperature_atm(altitude)/(273.15 + 15.0)) ** (-9.80665 / (287.05287 * (-6.5/1000)))
    if 20000 > altitude >= 11000:
        return 22632 * np.exp(-9.80665 * (altitude - 11000) / (287.05287 * temperature_atm(altitude)))
    if 32000 > altitude >= 20000:
        return 5474.9 * (temperature_atm(altitude)/(273.15 - 56.5)) ** (-9.80665 / (287.05287 * (1/1000)))
    if altitude >= 32000:
        print('atmospheric pressure/temperature model weak here')
        return 868.02

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