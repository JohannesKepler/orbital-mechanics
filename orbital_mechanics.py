# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 14:30:08 2018

@author: bw5177
"""

# F = G * M * m / r^2
# https://omniweb.gsfc.nasa.gov/coho/helios/planet.html
# http://ssd.jpl.nasa.gov/horizons.cgi

import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

orbital_parameters = pd.read_csv('orbital_table.csv', index_col = 0)

G = 6.67408 * 10**-11 # m^3 kg^-1 s^-2
SUN_MASS = 1.989 * 10**30 # kg
MU = G * SUN_MASS # m^3/s^2
#        week days hours minutes seconds
DELTA_T = 1 *  7   * 24   * 60    * 60

def get_dist(body_1, body_2):
    #print body_1
    #print body_2
    magnitude = math.sqrt((body_1[0] - body_2[0])**2 + (body_1[1] - body_2[1])**2 + (body_1[2] - body_2[2])**2)
    unit_vector = [(body_2[0] - body_1[0]) / magnitude, (body_2[1] - body_1[1]) / magnitude, (body_2[2] - body_1[2]) / magnitude]
    return (magnitude, unit_vector)

class CelestialBody:
    def __init__(self, body_name):
#        self.mass = mass
#        self.pos = pos
#        self.vel = vel
#        self.parent_body = parent_body
        self.orbital_parameters = orbital_parameters.loc[body_name]
        self.mass = float(self.orbital_parameters['Mass'])
        self.pos = [float(self.orbital_parameters['x']),
                    float(self.orbital_parameters['y']),
                    float(self.orbital_parameters['z'])]
        self.vel = [float(self.orbital_parameters['vx']),
                    float(self.orbital_parameters['vy']),
                    float(self.orbital_parameters['vz'])]

    def __str__(self):
        printable_mass = '{:0.2e}'.format(self.mass)
        printable_position = map(lambda x: '{:0.2e}'.format(x), self.pos)
        printable_velocity = map(lambda x: '{:0.2e}'.format(x), self.vel)
        printable_acceleration = map(lambda x: '{:0.2e}'.format(x), self.accel)
        return "Mass: %s\nPosition: %r\nVelocity: %r\nAccel: %r" % (printable_mass, printable_position,
                                                                    printable_velocity, printable_acceleration)

    def gravitate(self, other_body):
        r_mag, r_vector = get_dist(self.pos, other_body.pos)
        g_force_mag = G * self.mass * other_body.mass / (r_mag ** 2)
        g_force = map(lambda x: x*g_force_mag,r_vector)

        self.accel = map(lambda x: x / self.mass,g_force)
        self.vel = [(self.vel[x] + self.accel[x] * DELTA_T) for x in range(3)]
        self.pos = [(self.pos[x] + self.vel[x] * DELTA_T) for x in range(3)]
        #print self
#
#SUN_POS = [0,0,0] # m
#
## semi-major axis of orbit in meters
#ASTRO_UNIT = 1.496 * 10**11
#EARTH_DIST = ASTRO_UNIT
#MERCURY_DIST = 0.387 * ASTRO_UNIT
#VENUS_DIST = 0.723 * ASTRO_UNIT
#MARS_DIST = 1.524 * ASTRO_UNIT
#JUPITER_DIST = 5.203 * ASTRO_UNIT
#SATURN_DIST = 9.537 * ASTRO_UNIT
#URANUS_DIST = 19.191 * ASTRO_UNIT
#NEPTUNE_DIST = 30.069 * ASTRO_UNIT
#PLUTO_DIST = 39.482 * ASTRO_UNIT
#
## eccentricity of orbit, unitless
## eccentricity = 1 - (perihelion/semi-major axis)
#MERCURY_ECC = 0.2056
#VENUS_ECC = 0.0068
#EARTH_ECC = 0.0167
#MARS_ECC = 0.0934
#JUPITER_ECC = 0.0484
#SATURN_ECC = 0.0542
#URANUS_ECC = 0.0472
#NEPTUNE_ECC = 0.0086
#PLUTO_ECC = 0.2488
#
## orbital inclination in radians
#MERCURY_INC = 0.12226
#VENUS_INC = 0.059249
#EARTH_INC = 0
#MARS_INC = 0.032306
#JUPITER_INC = 0.022777
#SATURN_INC = 0.043354
#URANUS_INC = 0.013439
#NEPTUNE_INC = 0.030875
#PLUTO_INC = 0.299184
#
## longitude of ascending node
#
#EARTH_MASS = 5.9736 * 10**24 # kg
#MERCURY_MASS = 0.0553 * EARTH_MASS
#VENUS_MASS = 0.815 * EARTH_MASS
#MARS_MASS = 0.107 * EARTH_MASS
#JUPITER_MASS = 317.83 * EARTH_MASS
#SATURN_MASS = 95.159 * EARTH_MASS
#URANUS_MASS = 14.536 * EARTH_MASS
#NEPTUNE_MASS = 17.147 * EARTH_MASS
#PLUTO_MASS = 0.0021 * EARTH_MASS
#earth_pos = [EARTH_DIST, 0, 0] # m
#earth_vel = [0, 2.978 * 10**4, 0] # m/s

Sun = CelestialBody('Sun')
Earth = CelestialBody('Earth')
Mars = CelestialBody('Mars')
Jupiter = CelestialBody('Jupiter')

sun_x = []
sun_y = []
sun_z = []
earth_x = []
earth_y = []
earth_z = []
mars_x = []
mars_y = []
mars_z = []
jupiter_x = []
jupiter_y = []
jupiter_z = []
for i in range(500):
    Earth.gravitate(Sun)
    Mars.gravitate(Sun)
    Jupiter.gravitate(Sun)
    sun_x.append(Sun.pos[0])
    sun_y.append(Sun.pos[1])
    sun_z.append(Sun.pos[2])
    earth_x.append(Earth.pos[0])
    earth_y.append(Earth.pos[1])
    earth_z.append(Earth.pos[2])
    mars_x.append(Mars.pos[0])
    mars_y.append(Mars.pos[1])
    mars_z.append(Mars.pos[2])
    jupiter_x.append(Jupiter.pos[0])
    jupiter_y.append(Jupiter.pos[1])
    jupiter_z.append(Jupiter.pos[2])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(earth_x,earth_y,earth_z)
ax.scatter(mars_x,mars_y,mars_z)
ax.scatter(jupiter_x,jupiter_y,jupiter_z)

ax.set_xlabel('Ecliptic longitude')
ax.set_ylabel('Ecliptic latitude')
ax.set_zlabel('Azimuth')

plt.show()