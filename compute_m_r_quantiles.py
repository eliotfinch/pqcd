#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.constants import c, e, m_u
from scipy.interpolate import interp1d

collated_eos_path = '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

def weighted_quantile(values, quantiles, weights):

    sorter = np.argsort(values)
    values = values[sorter]
    weights = weights[sorter]

    weighted_quantiles = np.cumsum(weights)
    weighted_quantiles /= np.sum(weights)
    
    return np.interp(quantiles, weighted_quantiles, values)

# -----------------------------------------------------------------------------

# Load the collated EoSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)
nonzero_collated_eos = collated_eos[collated_eos.logweight_total > -np.inf]

# The pre-computed weights of these EoSs
weights = np.exp(nonzero_collated_eos.logweight_total.values)

# Load the full EoS data from the GP draws, and interpolate onto a consistent
# mass grid

mass_grid = np.linspace(0.8, 2.2, 1000)
radius_interp = []

for eos in nonzero_collated_eos.eos:

    eos = int(eos)

    df = pd.read_csv(f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/macro-draw-{eos:06}.csv')

    radius = df.R.values
    mass = df.M.values

    radius_interp.append(interp1d(mass, radius, fill_value='extrapolate')(mass_grid))

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
np.savetxt('weighted_quantiles/weighted_quantiles_mass_radius.dat', weighted_quantiles)
np.savetxt('weighted_quantiles/weighted_quantiles_combined_mass_radius_10.dat', weighted_quantiles_combined)
