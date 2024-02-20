#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from pQCD import pQCD

from utils import to_nucleons_per_cubic_femtometre

collated_eos_path = [
    'collated_np_all_post.csv', 
    '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
    ][1]

def qcd_likelihood(e_list, p_list, n_list, N=1000):
    """
    A modified qcd_likelihood function that, for a given random X sample, 
    computes the likelihood at a list of densities.
    """
    weights = np.zeros(len(n_list))

    for _ in range(N):
        
        X = np.random.uniform(np.log(1/2), np.log(2))
        pQCDX = pQCD(np.exp(X))
        
        for i, (e, p, n) in enumerate(zip(e_list, p_list, n_list)):
            weights[i] += int(pQCDX.constraints(e0=e,p0=p,n0=n))

    return weights/N

# -----------------------------------------------------------------------------

# Load the collated EOSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)
nonzero_collated_eos = collated_eos[collated_eos.logweight_total > -np.inf]

# The pre-computed weights of these EOSs
weights = np.exp(nonzero_collated_eos.logweight_total.values)

# The central density for which the mass reaches a maximum Mmax
collated_ntov = to_nucleons_per_cubic_femtometre(nonzero_collated_eos['rhoc(M@Mmax)'])

# Nuclear saturation density in fm^-3
nsat = 0.16

# -----------------------------------------------------------------------------

# Compute the pQCD likelihood at some particular matching densities

# The fixed-density matching densties to use
fixed_matching_densities = np.array([1,2,3,4,5,6,7,8,9,10])*nsat

# Load the pre-computed energy densities and pressures for each EOS for each
# matching density
fixed_energy_densities = np.array([
    np.loadtxt(f'fixed_n_quantities/energy_density_{int(n/nsat):02}nsat.dat') 
    for n in fixed_matching_densities
    ])

fixed_pressures = np.array([
    np.loadtxt(f'fixed_n_quantities/pressure_{int(n/nsat):02}nsat.dat') 
    for n in fixed_matching_densities
    ])

qcd_weights = []

# Load the nTOV quantities
ntov_energy_density = np.loadtxt('ntov_quantities/energy_density.dat')
ntov_pressure = np.loadtxt('ntov_quantities/pressure.dat')

for eos_number in range(len(nonzero_collated_eos)):

    e_list = fixed_energy_densities[:,eos_number]
    p_list = fixed_pressures[:,eos_number]

    e_list = np.append(e_list, ntov_energy_density[eos_number])
    p_list = np.append(p_list, ntov_pressure[eos_number])

    ntov = collated_ntov.iloc[eos_number]
    matching_densities = np.append(fixed_matching_densities, ntov)

    qcd_weights.append(qcd_likelihood(e_list, p_list, matching_densities))
    
qcd_weights = np.array(qcd_weights)

# Each row of qcd_weights is the weights for a particular EOS at a range of
# matching densities. It is more convenient to have the weights grouped by 
# matching density (i.e., columns of qcd_weights). 

# Save the fixed-density weights to disk
for i, n in enumerate(fixed_matching_densities):
    np.savetxt(f'weights/qcd_weights_ns{int(n/nsat):02}_Xmarg_shared.dat', qcd_weights[:,i])

# Save the nTOV weights to disk
np.savetxt('weights/qcd_weights_ntov_Xmarg_shared.dat', qcd_weights[:,-1])