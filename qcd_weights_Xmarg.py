#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d
from pQCD import pQCD

from utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
    nsat
)

# matching_density = float(sys.argv[1])*0.15

collated_eos_path = '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

def qcd_likelihood(e, p, n, N=1000):

    weight = np.zeros(N)

    for i in range(N):
        
        X = np.random.uniform(np.log(1/2), np.log(2)) # Log-linear distribution
        pQCDX = pQCD(np.exp(X)) # Redefine class with new X
        
        # For each X assign 0 or 1 for given point
        weight[i] = int(pQCDX.constraints(e0=e,p0=p,n0=n))

    return weight.mean()

# -----------------------------------------------------------------------------

# Load the collated EOSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)
nonzero_collated_eos = collated_eos[collated_eos.logweight_total > -np.inf]

# The pre-computed weights of these EOSs
weights = np.exp(nonzero_collated_eos.logweight_total.values)

# The central density for which the mass reaches a maximum Mmax
ntov = to_nucleons_per_cubic_femtometre(nonzero_collated_eos['rhoc(M@Mmax)'])

# Compute the QCD weights at a particular matching density

for matching_density in nsat*np.array([5,10,15]):

    qcd_weights = []
    errors = []

    for eos in nonzero_collated_eos.eos:

        eos = int(eos)

        df = pd.read_csv(f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/eos-draw-{eos:06}.csv')

        pressure = to_GeV_per_cubic_femtometre(df.pressurec2).values
        energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2).values
        number_density = to_nucleons_per_cubic_femtometre(df.baryon_density).values

        index = np.argmin(np.abs(number_density - matching_density))

        errors.append(np.min(np.abs(number_density - matching_density)))
        qcd_weights.append(
            qcd_likelihood(energy_density[index], pressure[index], number_density[index])
            )

    qcd_weights = np.array(qcd_weights)
    errors = np.array(errors)

    # Save the weights to disk
    np.savetxt(f'new_weights/qcd_weights_ns{int(matching_density/nsat):02}_Xmarg.dat', qcd_weights)

    # Save the errors to disk
    np.savetxt(f'new_weights/nterm_errors_ns{int(matching_density/nsat):02}_Xmarg.dat', errors)