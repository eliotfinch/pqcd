#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from pqcd.utils import to_GeV_per_cubic_femtometre

gp_number = 2
eos_dir = f'/home/eliot.finch/eos/pqcd/data/eos-draws-modified/gp{gp_number}'

collated_eos = pd.read_csv(
    f'{eos_dir}/eos-draws-modified-gp{gp_number}.csv'
)

cs2max_list = []

for n, eos in collated_eos.iterrows():

    df = pd.read_csv(
        f'{eos_dir}/margagn/DRAWmod1000-{n//1000:06}/eos-draw-{n:06}.csv'
    )

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2).values
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2).values
    speed_of_sound_squared = np.gradient(pressure, energy_density)

    cs2max_list.append(np.max(speed_of_sound_squared))

# Save to disk
np.savetxt(f'{eos_dir}/cs2max.dat', cs2max_list)
