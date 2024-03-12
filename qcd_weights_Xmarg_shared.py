#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from qcd_likelihood import pQCD

from utils import to_nucleons_per_cubic_femtometre, nsat

collated_eos_path = [
    'collated_eos.csv',
    'collated_np_all_post.csv', 
    '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
    ][0]

def pQCD_likelihood(e_list, p_list, n_list, N=1000):
    """
    A modified qcd_likelihood function that, for a given random X sample, 
    computes the likelihood at a list of densities.
    """
    weights = np.zeros(len(n_list))

    for _ in range(N):
        
        X = np.random.uniform(np.log(1/2), np.log(2))
        pQCDX = pQCD(np.exp(X))
        
        for i, (e, p, n) in enumerate(zip(e_list, p_list, n_list)):
            if np.isnan(p) or np.isnan(e):
                weights[i] += 0
            else:
                weights[i] += int(pQCDX.constraints(e0=e,p0=p,n0=n))

    return weights/N

# -----------------------------------------------------------------------------

# Load the collated EOSs 
collated_eos = pd.read_csv(collated_eos_path)

# The central density for which the mass reaches a maximum Mmax
collated_ntov = to_nucleons_per_cubic_femtometre(collated_eos['rhoc(M@Mmax)'])

# Compute the pQCD likelihood at some particular matching densities

# The fixed-density matching densties to use
fixed_matching_densities = np.array([1,2,3,4,5,6,7,8,9,10,15,20])

# Load the pre-computed pressures and energy densities for each EOS for each
# matching density
fixed_pressures = np.array([
    np.loadtxt(f'quantities_at_fixed_n/pressure_{n:02}nsat.dat') 
    for n in fixed_matching_densities
    ])

fixed_energy_densities = np.array([
    np.loadtxt(f'quantities_at_fixed_n/energy_density_{n:02}nsat.dat') 
    for n in fixed_matching_densities
    ])

# Load the nTOV quantities
ntov_pressure = np.loadtxt('quantities_at_ntov/pressure.dat')
ntov_energy_density = np.loadtxt('quantities_at_ntov/energy_density.dat')

qcd_weights = []

for eos_number in range(len(collated_ntov)):

    p_list = fixed_pressures[:,eos_number]
    e_list = fixed_energy_densities[:,eos_number]

    p_list = np.append(p_list, ntov_pressure[eos_number])
    e_list = np.append(e_list, ntov_energy_density[eos_number])

    ntov = collated_ntov.iloc[eos_number]
    matching_densities = np.append(fixed_matching_densities*nsat, ntov)

    qcd_weights.append(pQCD_likelihood(e_list, p_list, matching_densities))
    
qcd_weights = np.array(qcd_weights)

# Each row of qcd_weights is the weights for a particular EOS at a range of
# matching densities. It is more convenient to have the weights grouped by 
# matching density (i.e., columns of qcd_weights). 

# Save the fixed-density weights to disk
for i, n in enumerate(fixed_matching_densities):
    np.savetxt(f'weights_Xmarg_shared/qcd_weights_{n:02}nsat_Xmarg_shared.dat', qcd_weights[:,i])

# Save the nTOV weights to disk
np.savetxt('weights_Xmarg_shared/qcd_weights_ntov_Xmarg_shared.dat', qcd_weights[:,-1])