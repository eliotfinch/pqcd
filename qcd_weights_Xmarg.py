#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from qcd_likelihood import pQCD

from utils import to_nucleons_per_cubic_femtometre, nsat

collated_eos_path = [
    '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv',
    'collated_eos.csv'
    ][1]
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

def pQCD_likelihood(e, p, n, N=1000):

    weight = np.zeros(N)

    for i in range(N):
        
        X = np.random.uniform(np.log(1/2), np.log(2)) # Log-linear distribution
        pQCDX = pQCD(np.exp(X)) # Redefine class with new X
        
        # For each X assign 0 or 1 for given point
        weight[i] = int(pQCDX.constraints(e0=e,p0=p,n0=n))

    return weight.mean()

# -----------------------------------------------------------------------------

# Load the collated EOSs 
collated_eos = pd.read_csv(collated_eos_path)

# The central density for which the mass reaches a maximum Mmax
collated_ntov = to_nucleons_per_cubic_femtometre(collated_eos['rhoc(M@Mmax)'])

# Compute the pQCD weights at a particular nterm
nterm_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
qcd_weights = {nterm: [] for nterm in nterm_list}

for nterm in nterm_list:

    # Load the pre-computed pressure and energy density for each EOS at this
    # density
    pressure = np.loadtxt(f'quantities_at_fixed_n/pressure_{nterm:02}nsat.dat')
    energy_density = np.loadtxt(f'quantities_at_fixed_n/energy_density_{nterm:02}nsat.dat')

    # Compute the pQCD likelihood at this density
    for p, e in zip(pressure, energy_density):
        if np.isnan(p) or np.isnan(e):
            qcd_weights[nterm].append(0)
        else:
            qcd_weights[nterm].append(pQCD_likelihood(e, p, nterm*nsat))

# Save the weights to disk
for nterm in nterm_list:
    np.savetxt(f'weights/qcd_weights_{nterm:02}nsat_Xmarg.dat', qcd_weights[nterm])

# Compute the pQCD weights at nTOV
qcd_weights_ntov = []

pressure_tov = np.loadtxt('quantities_at_ntov/pressure.dat')
energy_density_tov = np.loadtxt('quantities_at_ntov/energy_density.dat')

for ntov, p, e in zip(collated_ntov, pressure_tov, energy_density_tov):
    qcd_weights_ntov.append(pQCD_likelihood(e, p, ntov))

np.savetxt('weights/qcd_weights_ntov_Xmarg.dat', qcd_weights_ntov)