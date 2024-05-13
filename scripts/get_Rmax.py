#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from pqcd.utils import eos_dir

collated_eos_path = '../data/eos-draws-default.csv'

# Load the collated EOSs
collated_eos = pd.read_csv(collated_eos_path)

Rmax = []

for eos in collated_eos.eos:

    eos = int(eos)

    df = pd.read_csv(f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/macro-draw-{eos:06}.csv')

    mass = df.M
    radius = df.R

    Rmax.append(radius[np.argmax(mass)])

Rmax = np.array(Rmax)

# Save to disk
np.savetxt('../data/ntov_quantities/radius.dat', Rmax)