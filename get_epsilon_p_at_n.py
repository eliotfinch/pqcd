#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d

from utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
)

collated_eos_path = '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

# Load the collated EOSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)
nonzero_collated_eos = collated_eos[collated_eos.logweight_total > -np.inf]

# The central density for which the mass reaches a maximum Mmax
ntov_array = to_nucleons_per_cubic_femtometre(nonzero_collated_eos['rhoc(M@Mmax)'])

# Nuclear saturation density in fm^-3
nsat = 0.16

# Load the full EoS data from the GP draws, and interpolate onto a consistent
# energy density grid

energy_density_grid = np.linspace(1e-10, 5, 1000)
pressure_interp = []
number_density_interp = []

for eos in nonzero_collated_eos.eos:

    eos = int(eos)

    df = pd.read_csv(f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/eos-draw-{eos:06}.csv')

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2).values
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2).values
    number_density = to_nucleons_per_cubic_femtometre(df.baryon_density).values

    pressure_interp.append(interp1d(energy_density, pressure)(energy_density_grid))
    number_density_interp.append(interp1d(energy_density, number_density)(energy_density_grid))

pressure_interp = np.array(pressure_interp)
number_density_interp = np.array(number_density_interp)

# Get the energy density and pressure at ntov

e_list = []
p_list = []

for p_grid, n_grid, ntov in zip(pressure_interp, number_density_interp, ntov_array):

    index = np.argmin(np.abs(n_grid - ntov))
    e = energy_density_grid[index]
    p = p_grid[index]

    e_list.append(e)
    p_list.append(p)

e_list = np.array(e_list)
p_list = np.array(p_list)

# Save to disk
np.savetxt('ntov_quantities/energy_density.dat', e_list)
np.savetxt('ntov_quantities/pressure.dat', p_list)

# Get the energy density and pressure at a fixed number density

# n0_list = np.array([1,3,5,7,9,10])*nsat

# for n0 in n0_list:

#     e_list = []
#     p_list = []

#     for p_grid, n_grid in zip(pressure_interp, number_density_interp):

#         index = np.argmin(np.abs(n_grid - n0))
#         e = energy_density_grid[index]
#         p = p_grid[index]

#         e_list.append(e)
#         p_list.append(p)

#     e_list = np.array(e_list)
#     p_list = np.array(p_list)

#     # Save to disk
#     np.savetxt(f'fixed_n_quantities/energy_density_{int(n0/nsat):02}nsat.dat', e_list)
#     np.savetxt(f'fixed_n_quantities/pressure_{int(n0/nsat):02}nsat.dat', p_list)
