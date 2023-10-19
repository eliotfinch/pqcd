#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

import sys

from scipy.constants import c, e, m_u
from scipy.interpolate import interp1d
from pQCD import pQCD

matching_density = float(sys.argv[1])*0.15

collated_eos_path = '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

def to_GeV_per_cubic_femtometre(x):

    # Convert to J/cm^3
    x = x*c**2/1000

    # Convert to GeV/fm^3
    return x*(1/(1e9*e))*((1e-15)**3/(0.01**3))

def to_nucleons_per_cubic_femtometre(x):

    # Convert to kg/fm^3
    x = (x/1000)*((1e-15)**3/(0.01**3))

    # Divide by the atomic mass constant to get nucleons/fm^3
    return x/m_u

def weighted_quantile(values, quantiles, weights):

    sorter = np.argsort(values)
    values = values[sorter]
    weights = weights[sorter]

    weighted_quantiles = np.cumsum(weights)
    weighted_quantiles /= np.sum(weights)
    
    return np.interp(quantiles, weighted_quantiles, values)

def qcd_likelihood(e, p, n, N=1000):

    weight = np.zeros(N)

    for i in range(N):
        
        X = np.random.uniform(np.log(1/2), np.log(2)) # Log-linear distribution
        pQCDX = pQCD(np.exp(X)) # Redefine class with new X
        
        # For each X assign 0 or 1 for given point
        weight[i] = int(pQCDX.constraints(e0=e,p0=p,n0=n))

    return weight.mean()

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

# Compute the QCD weights at a particular matching density

qcd_weights = []

for p_grid, n_grid in zip(pressure_interp, number_density_interp):

    # Find the pressure and energy density at the chosen matching density
    index = np.argmin(np.abs(n_grid - matching_density))
    e = energy_density_grid[index]
    p = p_grid[index]

    qcd_weights.append(qcd_likelihood(e, p, matching_density))

qcd_weights = np.array(qcd_weights)

# Save the weights to disk
np.savetxt(f'weights/qcd_weights_{matching_density/0.15}.dat', qcd_weights)