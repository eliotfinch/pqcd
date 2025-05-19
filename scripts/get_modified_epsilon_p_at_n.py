#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d

from pqcd.utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
)

gp_number = 2
eos_dir = f'/home/eliot.finch/eos/pqcd/data/eos-draws-modified/gp{gp_number}'

collated_eos = pd.read_csv(
    f'{eos_dir}/eos-draws-modified-gp{gp_number}.csv'
)

# The number densities (in nsat) at which to extract the energy density and
# pressure
n0_list = [2]

# Dicts to store the pressures and energy densities at the requested densities
p0_dict = {n0: [] for n0 in n0_list}
e0_dict = {n0: [] for n0 in n0_list}

for n, eos in collated_eos.iterrows():

    df = pd.read_csv(
        f'{eos_dir}/margagn/DRAWmod1000-{n//1000:06}/eos-draw-{n:06}.csv'
    )

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2).values
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2).values
    number_density = to_nucleons_per_cubic_femtometre(df.baryon_density).values

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

# Save to disk

destination_dir = f'{eos_dir}/quantities_at_n'

for n0 in n0_list:
    np.savetxt(f'{destination_dir}/pressure_{n0:02}nsat.dat', p0_dict[n0])
    np.savetxt(
        f'{destination_dir}/energy_density_{n0:02}nsat.dat', e0_dict[n0]
    )
