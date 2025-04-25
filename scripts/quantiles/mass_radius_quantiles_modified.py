#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

from scipy.interpolate import interp1d

from pqcd.utils import weighted_quantile

# Mass values
y_mr = np.linspace(0.5, 2.5, 1000)

gp_number = 2

eos_dir = f'/home/eliot.finch/eos/pqcd/data/eos-draws-modified/gp{gp_number}'
dest_dir = (
    '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
    f'gp{gp_number}/quantiles/'
)

collated_eos_gp1 = pd.read_csv(
    f'{eos_dir}/eos-draws-modified-gp{gp_number}.csv'
)

astro_weights = np.exp(
    collated_eos_gp1.logweight_total - collated_eos_gp1.logweight_total.max()
).values

r_interp = []

for n in collated_eos_gp1.eos:

    macro = pd.read_csv(
        f'{eos_dir}/margagn/DRAWmod1000-{n//1000:06}/macro-eos-draw-{n:06}.csv'
        )

    mass = macro.M.values
    radius = macro.R.values

    radius_mask = radius < 50
    mass = mass[radius_mask]
    radius = radius[radius_mask]

    mmax = np.max(mass)
    mmax_index = np.argmax(mass)

    r_interp.append(
        interp1d(
            mass[:mmax_index],
            radius[:mmax_index],
            bounds_error=False
        )(y_mr)
    )

r_interp = np.array(r_interp)

prior_quantiles = []
astro_quantiles = []

for i in range(len(y_mr)):
    prior_quantiles.append(
        weighted_quantile(
            r_interp[:, i],
            [0.05, 0.5, 0.95],
            weights=np.ones(len(r_interp))
        )
    )
    astro_quantiles.append(
        weighted_quantile(
            r_interp[:, i],
            [0.05, 0.5, 0.95],
            weights=astro_weights
        )
    )

prior_quantiles = np.array(prior_quantiles).T
astro_quantiles = np.array(astro_quantiles).T

np.savetxt(f'{dest_dir}/r_of_m_quantiles_prior.dat', prior_quantiles)
np.savetxt(f'{dest_dir}/r_of_m_quantiles_astro.dat', astro_quantiles)
