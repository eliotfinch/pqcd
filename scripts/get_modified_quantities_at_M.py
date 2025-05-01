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

Mstar_list = [1.4, 2.0]
for Mstar in Mstar_list:

    Lambdastar = []
    Rstar = []
    pc = []
    epsilonc = []

    for eos, entry in collated_eos.iterrows():

        eos = int(eos)

        macro = pd.read_csv(
            f'{eos_dir}/margagn/DRAWmod1000-{eos//1000:06}/'
            f'macro-eos-draw-{eos:06}.csv'
        )

        radius = macro.R.values
        radius_mask = radius < 30

        mass = macro.M.values[radius_mask]
        radius = radius[radius_mask]
        Lambda = macro.Lambda.values[radius_mask]
        central_density = to_nucleons_per_cubic_femtometre(
            macro.central_baryon_density.values[radius_mask]
        )

        turn_index = np.argmax(mass)
        mass = mass[:turn_index]
        radius = radius[:turn_index]
        Lambda = Lambda[:turn_index]
        central_density = central_density[:turn_index]

        if Mstar > max(mass):
            Rstar.append(np.nan)
            Lambdastar.append(np.nan)
            pc.append(np.nan)
            epsilonc.append(np.nan)
            continue

        index = np.argmin(np.abs(mass - Mstar))
        nc = central_density[index]

        df = pd.read_csv(
            f'{eos_dir}/margagn/DRAWmod1000-{eos//1000:06}/'
            f'eos-draw-{eos:06}.csv'
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

        # Extract quantities at nTOV
        Rstar.append(radius[index])
        Lambdastar.append(Lambda[index])
        pc.append(pressure_interp(nc))
        epsilonc.append(energy_density_interp(nc))

    # Save to disk
    np.savetxt(
        f'{eos_dir}/quantities_at_M/radius_{Mstar}.dat', Rstar
    )
    np.savetxt(
        f'{eos_dir}/quantities_at_M/Lambda_{Mstar}.dat', Lambdastar
    )
    np.savetxt(
        f'{eos_dir}/quantities_at_M/central_pressure_{Mstar}.dat', pc
    )
    np.savetxt(
        f'{eos_dir}/quantities_at_M/central_energy_density_{Mstar}.dat',
        epsilonc
    )
