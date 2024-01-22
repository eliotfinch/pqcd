#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

collated_eos_path = '/home/isaac.legred/PTAnalysis/Analysis/collated_np_all_post.csv'
eos_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn'

# Load the collated EOSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)
nonzero_collated_eos = collated_eos[collated_eos.logweight_total > -np.inf]

Rmax = []

for eos in nonzero_collated_eos.eos:

    eos = int(eos)

    df = pd.read_csv(f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/macro-draw-{eos:06}.csv')

    mass = df.M
    radius = df.R

    Rmax.append(radius[np.argmax(mass)])

Rmax = np.array(Rmax)

# Save to disk
np.savetxt('ntov_quantities/radius.dat', Rmax)