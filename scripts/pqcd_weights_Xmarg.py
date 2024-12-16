#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

import pqcd

from pqcd.utils import to_nucleons_per_cubic_femtometre, nsat

collated_eos_path = '../data/eos-draws-default/collated_np_all_post.csv'


def pQCD_likelihood(e, p, n, N=1000):

    weight = np.zeros(N)

    for i in range(N):

        logX = np.random.uniform(np.log(1/2), np.log(2))

        # For each X assign 0 or 1 for given point
        weight[i] = int(pqcd.maximised_likelihood(
            e0=e, p0=p, n0=n, X=np.exp(logX)
        ))

    return weight.mean()


# -----------------------------------------------------------------------------


# Load the collated EOSs
collated_eos = pd.read_csv(collated_eos_path)

# The central density for which the mass reaches a maximum Mmax
collated_ntov = to_nucleons_per_cubic_femtometre(collated_eos['rhoc(M@Mmax)'])

# Compute the pQCD weights at a particular nterm
nterm_list = [3, 5, 7, 9]  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
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
        if np.isnan(e) or np.isnan(p):
            qcd_weights[nterm].append(0)
        else:
            qcd_weights[nterm].append(pQCD_likelihood(e, p, nterm*nsat))

# Save the weights to disk
for nterm in nterm_list:
    np.savetxt(
        '../data/eos-draws-default/pqcd-weights/'
        f'pqcd_weights_{nterm:02}nsat_Xmarg_mu2.6.dat',
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
#     qcd_weights_ntov.append(pQCD_likelihood(e, p, ntov))

# np.savetxt(
#     '../data/eos-draws-default/pqcd-weights/'
#     '/pqcd_weights_ntov_Xmarg_mu2.6.dat',
#     qcd_weights_ntov
# )
