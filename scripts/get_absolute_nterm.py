#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from pqcd.utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
    eos_dir
)

collated_eos_path = '../data/eos-draws-default/collated_np_all_post.csv'
collated_eos = pd.read_csv(collated_eos_path)

pterm = []
epsilon_term = []
nterm = []

for eos in collated_eos.eos:

    eos = int(eos)

    df = pd.read_csv(
        f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/eos-draw-{eos:06}.csv'
    )

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2).values
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2).values
    number_density = to_nucleons_per_cubic_femtometre(df.baryon_density).values

    if len(pressure) == len(energy_density) == len(number_density):
        pterm.append(pressure[-1])
        epsilon_term.append(energy_density[-1])
        nterm.append(number_density[-1])
    else:
        print(f'eos {eos} not equal length!')

np.savetxt('../data/eos-draws-default/eos-draws-default-pterm.dat', pterm)
np.savetxt(
    '../data/eos-draws-default/eos-draws-default-epsilon_term.dat',
    epsilon_term
)
np.savetxt('../data/eos-draws-default/eos-draws-default-nterm.dat', nterm)
