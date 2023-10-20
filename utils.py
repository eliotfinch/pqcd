import numpy as np

from scipy.constants import c, e, m_u

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