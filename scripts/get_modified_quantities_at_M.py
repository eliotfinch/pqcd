#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d
from pqcd.utils import (
    to_nucleons_per_cubic_femtometre,
    to_GeV_per_cubic_femtometre,
)

gp_number = 2
eos_dir = f'/home/eliot.finch/eos/pqcd/data/eos-draws-modified/gp{gp_number}'

collated_eos = pd.read_csv(
    f'{eos_dir}/eos-draws-modified-gp{gp_number}.csv'
)

Mstar_list = [0.5, 1.0, 1.4, 2.0]
for Mstar in Mstar_list:

    Rstar = []
    pc = []
    epsilonc = []

    for eos, entry in collated_eos.iterrows():

        eos = int(eos)

        macro = pd.read_csv(
            f'{eos_dir}/DRAWmod1000-{eos//1000:06}/macro-eos-draw-{eos:06}.csv'
        )

        mass = macro.M
        radius = macro.R
        central_density = to_nucleons_per_cubic_femtometre(
            macro.central_baryon_density
        )

        index = np.argmin(np.abs(mass - Mstar))
        nc = central_density[index]

        df = pd.read_csv(
            f'{eos_dir}/DRAWmod1000-{eos//1000:06}/eos-draw-{eos:06}.csv'
        )

        pressure = to_GeV_per_cubic_femtometre(df.pressurec2)
        energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2)
        number_density = to_nucleons_per_cubic_femtometre(df.baryon_density)

        # Build an interpolant over number density
        pressure_interp = interp1d(
            number_density, pressure, bounds_error=False
        )
        energy_density_interp = interp1d(
            number_density, energy_density, bounds_error=False
        )

        # Extract quantities at nTOV. If outside the range of the EOS, a nan is
        # returned.
        Rstar.append(radius[index])
        pc.append(pressure_interp(nc))
        epsilonc.append(energy_density_interp(nc))

    # Save to disk
    np.savetxt(
        f'../data/eos-draws-default/quantities_at_M/radius_{Mstar}.dat', Rstar
    )
    np.savetxt(
        '../data/eos-draws-default/quantities_at_M/'
        f'central_pressure_{Mstar}.dat',
        pc
    )
    np.savetxt(
        '../data/eos-draws-default/quantities_at_M/'
        f'central_energy_density_{Mstar}.dat',
        epsilonc
    )
