#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from pqcd.utils import (
    to_nucleons_per_cubic_femtometre,
    to_GeV_per_cubic_femtometre,
    rcparams,
    eos_dir
)
plt.rcParams.update(rcparams)

collated_eos_gp0 = pd.read_csv(
    '../data/eos-draws-default/eos-draws-default.csv',
    index_col='eos'
)

Mstar = 0.5

# Rstar = []
# pc = []
# epsilonc = []
nc_list = []

for eos, entry in collated_eos_gp0.iterrows():

    eos = int(eos)

    macro = pd.read_csv(
        f'{eos_dir}/DRAWmod1000-{eos//1000:06}/macro-draw-{eos:06}.csv'
    )

    mass = macro.M
    radius = macro.R
    central_density = to_nucleons_per_cubic_femtometre(macro.rhoc)

    index = np.argmin(np.abs(mass - Mstar))
    nc = central_density[index]

    df = pd.read_csv(
        f'{eos_dir}/DRAWmod1000-{eos//1000:06}/eos-draw-{eos:06}.csv'
    )

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2)
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2)
    number_density = to_nucleons_per_cubic_femtometre(df.baryon_density)

    # Build an interpolant over number density
    pressure_interp = interp1d(number_density, pressure, bounds_error=False)
    energy_density_interp = interp1d(
        number_density, energy_density, bounds_error=False
    )

    # Extract quantities at nc
    # Rstar.append(radius[index])
    # pc.append(pressure_interp(nc))
    # epsilonc.append(energy_density_interp(nc))
    nc_list.append(nc)

# Save to disk
# np.savetxt(
#     f'../data/eos-draws-default/quantities_at_M/radius_{Mstar}.dat', Rstar
# )
# np.savetxt(
#     f'../data/eos-draws-default/quantities_at_M/central_pressure_{Mstar}.dat',
#     pc
# )
# np.savetxt(
#     '../data/eos-draws-default/quantities_at_M/'
#     f'central_energy_density_{Mstar}.dat',
#     epsilonc
# )
np.savetxt(
    '../data/eos-draws-default/quantities_at_M/'
    f'central_baryon_density_{Mstar}.dat',
    nc_list
)
