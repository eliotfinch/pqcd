#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d
from eos_marginalization import eos_marginalization

from utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
)

collated_eos_path = '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

eos_marg_cond = eos_marginalization()
qcd_likelihood = eos_marg_cond.marg_QCD_likelihood()

# -----------------------------------------------------------------------------

# Load the collated EoSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)
nonzero_collated_eos = collated_eos[collated_eos.logweight_total > -np.inf]

# The pre-computed weights of these EOSs
weights = np.exp(nonzero_collated_eos.logweight_total.values)

# The central density for which the mass reaches a maximum Mmax
ntov = to_nucleons_per_cubic_femtometre(nonzero_collated_eos['rhoc(M@Mmax)'])

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

# Compute the QCD weights at a particular nterm

qcd_weights = []
n_skipped = 0

for p_grid, n_grid, nterm in zip(pressure_interp, number_density_interp, ntov):

    # Requirement of the marginalized QCD likelihood
    if nterm < 35*0.16:

        # Find the pressure and energy density at the chosen nterm
        index = np.argmin(np.abs(n_grid - nterm))
        e = energy_density_grid[index]
        p = p_grid[index]

        qcd_weights.append(qcd_likelihood(e, p, nterm))

    else:

        n_skipped += 1
        qcd_weights.append(0)

qcd_weights = np.array(qcd_weights)
print(f'{n_skipped} EOSs skipped')

# Save the weights to disk
np.savetxt('test_weights/qcd_weights_marg.dat', qcd_weights)

for nterm in 0.15*np.array([2,4,6,8,10]):

    qcd_weights = []

    for p_grid, n_grid in zip(pressure_interp, number_density_interp):

        # Find the pressure and energy density at the chosen nterm
        index = np.argmin(np.abs(n_grid - nterm))
        e = energy_density_grid[index]
        p = p_grid[index]

        qcd_weights.append(qcd_likelihood(e, p, nterm))

    qcd_weights = np.array(qcd_weights)

    # Save the weights to disk
    np.savetxt(f'test_weights/qcd_weights_ns{int(nterm/0.15):02}_marg.dat', qcd_weights)