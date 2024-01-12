#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.constants import c, e, m_u
from scipy.interpolate import interp1d
from eos_marginalization import eos_marginalization

from utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
)

collated_eos_path = '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

eos_marg_cond = eos_marginalization()
qcd_likelihood = eos_marg_cond.marg_QCD_likelihood()

# -----------------------------------------------------------------------------

# Load the collated EoSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)
nonzero_collated_eos = collated_eos[collated_eos.logweight_total > -np.inf]

# The pre-computed weights of these EoSs
weights = np.exp(nonzero_collated_eos.logweight_total.values)

# Load the full EoS data from the GP draws, and get the energy density and 
# pressure at the final numebr density (which is the termination density?).
# Then evaliuate the new QCD likelihood at these values.

qcd_weights = []

for eos in nonzero_collated_eos.eos:

    eos = int(eos)

    df = pd.read_csv(f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/eos-draw-{eos:06}.csv')

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2).values[-1]
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2).values[-1]
    number_density = to_nucleons_per_cubic_femtometre(df.baryon_density).values[-1]

    qcd_weights.append(qcd_likelihood(energy_density, pressure, number_density))

qcd_weights = np.array(qcd_weights)

# Save the weights to disk
np.savetxt(f'weights/qcd_weights_marg.dat', qcd_weights)