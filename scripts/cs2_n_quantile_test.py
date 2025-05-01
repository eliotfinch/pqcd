#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d
from pqcd.utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
    weighted_quantile,
    eos_dir
    )

x_cn = to_nucleons_per_cubic_femtometre(np.linspace(2.8e13, 1.5e16, 1000))

# Collated EOSs
collated_eos_gp0 = pd.read_csv(
    '../data/eos-draws-default/eos-draws-default.csv',
    index_col='eos'
)
collated_eos_gp0_with_ntov = pd.read_csv(
    '../data/eos-draws-default/collated_np_all_post.csv',
    index_col='eos'
)
collated_eos_gp0['ntov'] = collated_eos_gp0_with_ntov['rhoc(M@Mmax)']

# Weights
astro_weights_gp0 = np.exp(
    collated_eos_gp0.logweight_total - collated_eos_gp0.logweight_total.max()
).values
ntov_marg_weights_gp0 = np.loadtxt(
    '../data/eos-draws-default/pqcd-weights/pqcd_weights_ntov_marg.dat'
)

cs2_interp = []

for eos, entry in collated_eos_gp0.iterrows():

    df = pd.read_csv(
        f'{eos_dir}/DRAWmod1000-{int(eos/1000):06}/eos-draw-{int(eos):06}.csv'
    )

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2)
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2)
    number_density = to_nucleons_per_cubic_femtometre(df.baryon_density)
    speed_of_sound_squared = np.gradient(pressure, energy_density)

    ntov = to_nucleons_per_cubic_femtometre(entry['ntov'])
    mask = number_density < ntov

    # Build an interpolant over number density
    cs2_interp.append(interp1d(
        number_density[mask], speed_of_sound_squared[mask], bounds_error=False
    )(x_cn))

cs2_interp = np.array(cs2_interp)

cs2_quantiles = []

for i in range(len(x_cn)):

    try:
        cs2_quantiles.append(
            weighted_quantile(
                cs2_interp[:, i][~np.isnan(cs2_interp[:, i])],
                [0.05, 0.5, 0.95],
                weights=(astro_weights_gp0*ntov_marg_weights_gp0)[
                    ~np.isnan(cs2_interp[:, i])
                ]
            )
        )
    except ValueError:
        cs2_quantiles.append([np.nan, np.nan, np.nan])

cs2_quantiles = np.array(cs2_quantiles).T

# Save the quantiles
np.savetxt(
    '../data/eos-draws-default/cs2_quantiles_test.dat',
    cs2_quantiles
)
