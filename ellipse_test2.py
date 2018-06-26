# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 12:16:28 2018

@author: bw5177
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np

earth_a = 1.00000365
earth_e = .01670311
earth_TA = 171.12052664 * np.pi / 180
earth_theta = np.linspace(0,earth_TA, 360)
earth_r = (earth_a*(1-earth_e**2))/(1+earth_e*np.cos(earth_theta))
plt.polar(earth_theta, earth_r)

mars_a = 1.52371375
mars_e = .09340867
mars_TA = 308.81129708 * np.pi / 180
mars_theta = np.linspace(0,mars_TA, 360)
mars_r = (mars_a*(1-mars_e**2))/(1+mars_e*np.cos(mars_theta))
plt.polar(mars_theta,mars_r)

#print(np.c_[earth_r, theta])

plt.show()