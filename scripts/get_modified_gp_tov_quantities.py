#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d

from pqcd.utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
)

gp_number = 1
eos_dir = f'/home/eliot.finch/eos/pqcd/data/eos-draws-modified/gp{gp_number}'

collated_eos = pd.read_csv(
    f'{eos_dir}/eos-draws-modified-gp{gp_number}.csv'
)

# Lists to store density, pressure and energy density at ntov
ntov_list = []
ptov_list = []
etov_list = []

for n, eos in collated_eos.iterrows():

    # Get nTOV

    Mmax = eos['Mmax']

    macro = pd.read_csv(
        f'{eos_dir}/margagn/DRAWmod1000-{n//1000:06}/macro-eos-draw-{n:06}.csv'
        )

    nc = to_nucleons_per_cubic_femtometre(macro.rhoc.values)
    mass = macro.M.values
    radius = macro.R.values

    ntov = nc[np.argmin(np.abs(mass-Mmax))]
    ntov_list.append(ntov)

    # Get pressure and energy density at nTOV

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

    # Extract the energy density and pressure at nTOV. If outside the range of
    # the EOS, a nan is returned.
    ptov_list.append(pressure_interp(ntov))
    etov_list.append(energy_density_interp(ntov))

# Save to disk

destination_dir = f'{eos_dir}/quantities_at_n'

np.savetxt(f'{destination_dir}/density_ntov.dat', ntov_list)
np.savetxt(f'{destination_dir}/pressure_ntov.dat', ptov_list)
np.savetxt(f'{destination_dir}/energy_density_ntov.dat', etov_list)
