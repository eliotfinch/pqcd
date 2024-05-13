import numpy as np

from scipy.constants import c, e, m_u

# The location on ldas-grid of the default EOS draws
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

# The value we use for the nuclear saturation density, in 1/fm^3. This follows,
# e.g., Komoltsev et al. arXiv:2312.14127
nsat = 0.16

rcparams = {
    'font.size': 14,
    'axes.titlesize': 14,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'font.family': 'serif',
    'font.sans-serif': ['Computer Modern Roman'],
    'text.usetex': True,
    }

# Our EOSs have pressure, energy density, and baryon density in units of 
# g/cm^3. These fucntions convert to units used by others for comparison.

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