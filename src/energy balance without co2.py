import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from parameters import stefan_boltzmann, average_earth_radius, average_sun_radius, earth_sun_distance

# set up fsolve
# solve basic energy balance equation
# for intensity from sun, use integration of e490 data?
# can initally use stefan boltzmann law to estimate intensity from sun

sun_intensity = (stefan_boltzmann * (5772)**4) * (average_sun_radius/earth_sun_distance)**2
albedo = 0.3
T_earth = (((np.pi * (average_earth_radius**2)) * sun_intensity * (1 - albedo)) / (stefan_boltzmann * (4 * np.pi * (average_earth_radius**2))))**(1/4)
print(T_earth)
print(sun_intensity)