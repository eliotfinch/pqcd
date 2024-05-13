#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from pqcd.likelihood import marginalised
from pqcd.utils import to_nucleons_per_cubic_femtometre, nsat

collated_eos_path = '../data/eos-draws-default.csv'

marg_cond = marginalised()
pQCD_likelihood = marg_cond.likelihood()

# -----------------------------------------------------------------------------

# Load the collated EOSs 
collated_eos = pd.read_csv(collated_eos_path)

# The central density for which the mass reaches a maximum Mmax
collated_ntov = to_nucleons_per_cubic_femtometre(collated_eos['rhoc(M@Mmax)'])

# Compute the pQCD weights at a particular nterm
nterm_list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
qcd_weights = {nterm: [] for nterm in nterm_list}

for nterm in nterm_list:

    # Load the pre-computed pressure and energy density for each EOS at this
    # density
    pressure = np.loadtxt(f'../data/quantities_at_fixed_n/pressure_{nterm:02}nsat.dat')
    energy_density = np.loadtxt(f'../data/quantities_at_fixed_n/energy_density_{nterm:02}nsat.dat')

    # Compute the pQCD likelihood at this density
    for p, e in zip(pressure, energy_density):
        if np.isnan(p) or np.isnan(e):
            qcd_weights[nterm].append(0)
        else:
            qcd_weights[nterm].append(pQCD_likelihood(n0=nterm*nsat, e0=e, p0=p))

# Save the weights to disk
for nterm in nterm_list:
    np.savetxt(f'../data/weights/qcd_weights_{nterm:02}nsat_marg.dat', qcd_weights[nterm])

# Compute the pQCD weights at nTOV
qcd_weights_ntov = []

pressure_tov = np.loadtxt('../data/quantities_at_ntov/pressure.dat')
energy_density_tov = np.loadtxt('../data/quantities_at_ntov/energy_density.dat')

for ntov, p, e in zip(collated_ntov, pressure_tov, energy_density_tov):
    
    # Requirement of the marginalized pQCD likelihood
    if ntov < 35*nsat:
        qcd_weights_ntov.append(pQCD_likelihood(n0=ntov, e0=e, p0=p))
    else:
        qcd_weights_ntov.append(0)

np.savetxt('../data/weights/qcd_weights_ntov_marg.dat', qcd_weights_ntov)