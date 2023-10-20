#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d
from utils import weighted_quantile

collated_eos_path = '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

# -----------------------------------------------------------------------------

# Load the collated EoSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)
nonzero_collated_eos = collated_eos[collated_eos.logweight_total > -np.inf]

# The pre-computed weights of these EoSs
weights = np.exp(nonzero_collated_eos.logweight_total.values)

# Load the full EoS data from the GP draws, and interpolate onto a consistent
# mass grid

mass_grid = np.linspace(0.8, 1.8, 1000)
radius_interp = []

for eos in nonzero_collated_eos.eos:

    eos = int(eos)

    df = pd.read_csv(f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/macro-draw-{eos:06}.csv')

    mass = df.M.values
    radius = df.R.values

    turning_index = np.argmax(mass)
    mass = mass[:turning_index]
    radius = radius[:turning_index]

    try:
        radius_interp.append(interp1d(mass, radius)(mass_grid))
    except:
        pass

radius_interp = np.array(radius_interp)

# Compute the weighted quantiles of the radius at each mass, using the 
# pre-computed weights
weighted_quantiles = []

for i in range(len(mass_grid)):
    weighted_quantiles.append(weighted_quantile(radius_interp[:,i], [0.05, 0.5, 0.95], weights=weights))

weighted_quantiles = np.array(weighted_quantiles).T

# Load the QCD weights at a particular matching density

qcd_weights = np.loadtxt('weights/qcd_weights_10.dat')

# Compute the weighted quantiles of the radius at each mass, using the combined 
# weights
combined_weights = weights*qcd_weights

weighted_quantiles_combined = []

for i in range(len(mass_grid)):
    weighted_quantiles_combined.append(weighted_quantile(radius_interp[:,i], [0.05, 0.5, 0.95], weights=combined_weights))

weighted_quantiles_combined = np.array(weighted_quantiles_combined).T

# Save the weighted quantiles to disk
np.savetxt('weighted_quantiles/weighted_quantiles_m_r.dat', weighted_quantiles)
np.savetxt('weighted_quantiles/weighted_quantiles_combined_m_r_10.dat', weighted_quantiles_combined)
