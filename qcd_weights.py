#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from qcd_likelihood import pQCD

from utils import to_nucleons_per_cubic_femtometre, nsat

collated_eos_path = [
    '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv',
    'collated_eos.csv'
    ][1]

def pQCD_likelihood(e, p, n, X):
    pQCDX = pQCD(np.exp(X)) # Redefine class with new X
    return int(pQCDX.constraints(e0=e,p0=p,n0=n))

# -----------------------------------------------------------------------------

# Load the collated EOSs 
collated_eos = pd.read_csv(collated_eos_path)

# The central density for which the mass reaches a maximum Mmax
collated_ntov = to_nucleons_per_cubic_femtometre(collated_eos['rhoc(M@Mmax)'])

# Compute the pQCD weights at a particular nterm and X
X_list = [0.5, 2]
nterm_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
qcd_weights = {nterm: {X: [] for X in X_list} for nterm in nterm_list}

for nterm in nterm_list:

    # Load the pre-computed energy density and pressure for each EOS at this
    # density
    energy_density = np.loadtxt(f'quantities_at_fixed_n/energy_density_{nterm:02}nsat.dat')
    pressure = np.loadtxt(f'quantities_at_fixed_n/pressure_{nterm:02}nsat.dat')

    # Compute the pQCD likelihood at this density
    for e, p in zip(energy_density, pressure):
        for X in X_list:
            if np.isnan(e) or np.isnan(p):
                qcd_weights[nterm][X].append(0)
            else:
                qcd_weights[nterm][X].append(pQCD_likelihood(e, p, nterm*nsat, X))

# Save the weights to disk
for nterm in nterm_list:
    for X in X_list:
        np.savetxt(f'weights/qcd_weights_{nterm:02}nsat_X{X}.dat', qcd_weights[nterm][X])

# Compute the pQCD weights at nTOV
qcd_weights_ntov = {X: [] for X in X_list}

energy_density_tov = np.loadtxt('quantities_at_ntov/energy_density.dat')
pressure_tov = np.loadtxt('quantities_at_ntov/pressure.dat')

for e, p, ntov in zip(energy_density_tov, pressure_tov, collated_ntov):
    for X in X_list:
        qcd_weights_ntov[X].append(pQCD_likelihood(e, p, ntov, X))

for X in X_list:
    np.savetxt(f'weights/qcd_weights_ntov_X{X}.dat', qcd_weights_ntov[X])