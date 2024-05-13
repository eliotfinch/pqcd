#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from pqcd.utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
    eos_dir
)

collated_eos_path = '../data/eos-draws-default.csv'

# Load the collated EOSs and filter out the ones with zero weight
collated_eos = pd.read_csv(collated_eos_path)

nterm = []

for eos in collated_eos.eos:

    eos = int(eos)

    df = pd.read_csv(f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/eos-draw-{eos:06}.csv')

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2).values
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2).values
    number_density = to_nucleons_per_cubic_femtometre(df.baryon_density).values

    nterm.append(number_density[-1])

nterm = np.array(nterm)

# Save the nterm to disk
np.savetxt(f'../data/eos-draws-default-nterm.dat', nterm)