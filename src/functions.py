from parameters import h
from parameters import c
from parameters import boltzmann
import math
import numpy as np
import matplotlib.pyplot as plt

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
    if altitude > 32000:
        print('atmospheric pressure/temperature model weak here')
        return 868.02

#Number density in atmosphere - derived from ideal gas law
def number_density(altitude):
    #accepts altitude above sea level
    #should take data from a source for pressure and temperature - later venture
    # currently uses sea level temperature (T=296K as used by HITRAN) and pressure (1 atm = 101325 Pa)
    temperature = temperature_atm(altitude)
    pressure = pressure_atm(altitude)
    return pressure/(boltzmann*temperature)

"""plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

altitude = np.linspace(0,32000, 50)
numbbbb = np.zeros(len(altitude))
for i in range(len(altitude)):
     numbbbb[i] = number_density(altitude[i])
ax.plot(
        altitude,
        numbbbb
        
        )
plt.show()"""

def spectral_irradiance(radius_of_source, distance, frequency, temperature):
    return np.pi * planck_spectrum(frequency, temperature) * (radius_of_source/distance)**2

def cross_section(wavenumber_index, wavenumber, altitude, spectral_line_intensity, wavenumber_array, pressure_broadening): # calculates cross section for a specific wavenumber
    temperature = 296
    pressure = 101325
    broadening_at_alt = (number_density(altitude)/(pressure/(boltzmann*temperature)))*pressure_broadening[wavenumber_index]    # we are adjusting the pressure broadening
    return (spectral_line_intensity[wavenumber_index] * broadening_at_alt) / (np.pi * (broadening_at_alt**2 + (wavenumber - wavenumber_array[wavenumber_index])**2))

def schwarzschild_equation(wavenumber, max_altitude, no_altitude_steps, spectral_line_intensity, wavenumber_array, pressure_broadening, earth_temperature): # calculates spectral radiance for a specific frequency/wavenumber
     # max altitude could be 32km, earth temperature could be 296K to start
     altitudes = np.linspace(0, max_altitude, no_altitude_steps)
     dz = max_altitude/no_altitude_steps
     initial_radiance = planck_spectrum(wavenumber*c, earth_temperature)
     spectral_radiances_dI = np.zeros(len(altitudes))
     for r in range(len(altitudes)):
         cross_section_sum = 0
         for i in range(len(wavenumber_array)):
             cross_section_sum += cross_section(i, wavenumber, altitudes[r], spectral_line_intensity, wavenumber_array, pressure_broadening)
         number_density_r = number_density(altitudes[r])
         planck_radiance_r = planck_spectrum(wavenumber*c, temperature_atm(altitudes[r]))
         spectral_radiances_dI[r] = dz * (-1 * number_density_r * cross_section_sum) * (spectral_radiances_dI[r-1] - planck_radiance_r)
     spectral_radiances_integral = 0
     for i in range(len(spectral_radiances_dI)):
          spectral_radiances_integral += spectral_radiances_dI[i]
     return spectral_radiances_integral