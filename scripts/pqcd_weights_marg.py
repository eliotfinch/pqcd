#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from pqcd.likelihood import marginalised
from pqcd.utils import to_nucleons_per_cubic_femtometre, nsat

collated_eos_path = '../data/eos-draws-default/collated_np_all_post.csv'

marg_cond = marginalised()
pQCD_likelihood = marg_cond.likelihood()

# -----------------------------------------------------------------------------

# Load the collated EOSs
collated_eos = pd.read_csv(collated_eos_path)

# The central density for which the mass reaches a maximum Mmax
collated_ntov = to_nucleons_per_cubic_femtometre(collated_eos['rhoc(M@Mmax)'])

# Compute the pQCD weights at a particular nterm
nterm_list = [2, 4, 6, 8]  # [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
qcd_weights = {nterm: [] for nterm in nterm_list}

for nterm in nterm_list:

    # Load the pre-computed pressure and energy density for each EOS at this
    # density
    energy_density = np.loadtxt(
        '../data/eos-draws-default/quantities_at_n/'
        f'energy_density_{nterm:02}nsat.dat'
    )
    pressure = np.loadtxt(
        '../data/eos-draws-default/quantities_at_n/'
        f'pressure_{nterm:02}nsat.dat'
    )

    # Compute the pQCD likelihood at this density
    for e, p in zip(energy_density, pressure):
        if np.isnan(p) or np.isnan(e):
            qcd_weights[nterm].append(0)
        else:
            qcd_weights[nterm].append(
                pQCD_likelihood(e0=e, p0=p, n0=nterm*nsat)
                )

# Save the weights to disk
for nterm in nterm_list:
    np.savetxt(
        '../data/eos-draws-default/pqcd-weights/'
        f'pqcd_weights_{nterm:02}nsat_marg.dat',
        qcd_weights[nterm]
    )

# Compute the pQCD weights at nTOV
# qcd_weights_ntov = []

# energy_density_tov = np.loadtxt(
#     '../data/eos-draws-default/quantities_at_n/energy_density_ntov.dat'
# )
# pressure_tov = np.loadtxt(
#     '../data/eos-draws-default/quantities_at_n/pressure_ntov.dat'
# )

# for e, p, ntov in zip(energy_density_tov, pressure_tov, collated_ntov):
#     # Requirement of the marginalized pQCD likelihood
#     if nsat < ntov < 35*nsat:
#         qcd_weights_ntov.append(pQCD_likelihood(e0=e, p0=p, n0=ntov))
#     else:
#         qcd_weights_ntov.append(0)

# np.savetxt(
#     '../data/eos-draws-default/pqcd-weights/'
#     'pqcd_weights_ntov_marg.dat',
#     qcd_weights_ntov
# )
