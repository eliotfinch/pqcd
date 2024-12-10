#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d

from pqcd.utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
    nsat,
    eos_dir
)

collated_eos_path = '../data/eos-draws-default/collated_np_all_post.csv'

# Load the collated EOSs
collated_eos = pd.read_csv(collated_eos_path)

# The central density for which the mass reaches a maximum Mmax
collated_ntov = \
    to_nucleons_per_cubic_femtometre(collated_eos['rhoc(M@Mmax)'])/nsat

# The number densities (in nsat) at which to extract the energy density and
# pressure
n0_list = [2, 4, 6, 8]  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]

# Dicts to store the pressures and energy densities at the requested densities
p0_dict = {n0: [] for n0 in n0_list}
e0_dict = {n0: [] for n0 in n0_list}

# Lists to store pressure and energy density at ntov
ptov_list = []
etov_list = []

# For each EOS, interpolate the pressure and energy density as a function of
# number density and extract quantities at the requested densities
for eos, ntov in zip(collated_eos.eos, collated_ntov):

    df = pd.read_csv(
        f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/eos-draw-{int(eos):06}.csv'
    )

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2).values
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2).values
    number_density = \
        to_nucleons_per_cubic_femtometre(df.baryon_density).values/nsat

    # Build an interpolant over number density
    pressure_interp = interp1d(number_density, pressure, bounds_error=False)
    energy_density_interp = interp1d(
        number_density, energy_density, bounds_error=False
    )

    # Extract the energy density and pressure at the required densities. If
    # outside the range of the EOS, a nan is returned.
    for n0 in n0_list:
        p0_dict[n0].append(pressure_interp(n0))
        e0_dict[n0].append(energy_density_interp(n0))

    ptov_list.append(pressure_interp(ntov))
    etov_list.append(energy_density_interp(ntov))

# Save to disk

destination_dir = '../data/eos-draws-default/quantities_at_n'

for n0 in n0_list:
    np.savetxt(f'{destination_dir}/pressure_{n0:02}nsat.dat', p0_dict[n0])
    np.savetxt(
        f'{destination_dir}/energy_density_{n0:02}nsat.dat', e0_dict[n0]
    )

# np.savetxt(f'{destination_dir}/pressure_ntov.dat', ptov_list)
# np.savetxt(f'{destination_dir}/energy_density_ntov.dat', etov_list)
