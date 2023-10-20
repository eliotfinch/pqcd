#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d
from utils import (
    to_GeV_per_cubic_femtometre, 
    to_nucleons_per_cubic_femtometre, 
    weighted_quantile
)

collated_eos_path = '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

# -----------------------------------------------------------------------------

# Load the collated EoSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)
nonzero_collated_eos = collated_eos[collated_eos.logweight_total > -np.inf]

# The pre-computed weights of these EoSs
weights = np.exp(nonzero_collated_eos.logweight_total.values)

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

# Compute the weighted quantiles of the pressure at each energy density, using
# the pre-computed weights
weighted_quantiles = []

for i in range(len(energy_density_grid)):
    weighted_quantiles.append(weighted_quantile(pressure_interp[:,i], [0.05, 0.5, 0.95], weights=weights))

weighted_quantiles = np.array(weighted_quantiles).T

# Load the QCD weights at a particular matching density

qcd_weights = np.loadtxt('weights/qcd_weights_10.dat')

# Compute the weighted quantiles of the pressure at each energy density, using
# the combined weights
combined_weights = weights*qcd_weights

weighted_quantiles_combined = []

for i in range(len(energy_density_grid)):
    weighted_quantiles_combined.append(weighted_quantile(pressure_interp[:,i], [0.05, 0.5, 0.95], weights=combined_weights))

weighted_quantiles_combined = np.array(weighted_quantiles_combined).T

# Save the weighted quantiles to disk
np.savetxt('weighted_quantiles/weighted_quantiles_p_e_test.dat', weighted_quantiles)
np.savetxt('weighted_quantiles/weighted_quantiles_combined_p_e_10_test.dat', weighted_quantiles_combined)
