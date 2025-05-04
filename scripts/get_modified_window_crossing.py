#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

import pqcd

from pqcd.utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
    )

gp_number = 2
eos_dir = f'/home/eliot.finch/eos/pqcd/data/eos-draws-modified/gp{gp_number}'

collated_eos = pd.read_csv(
    f'{eos_dir}/eos-draws-modified-gp{gp_number}.csv'
)

pqcd_region_dict = pqcd.get_pqcd_region(mu_low=2.4, mu_high=3, res=200)

mu_intersect = []

for n in collated_eos.eos:

    df = pd.read_csv(
        f'{eos_dir}/margagn/'
        f'DRAWmod1000-{int(n)//1000:06}/eos-draw-{int(n):06}.csv'
    )

    pressure = to_GeV_per_cubic_femtometre(df.pressurec2)
    energy_density = to_GeV_per_cubic_femtometre(df.energy_densityc2)
    number_density = to_nucleons_per_cubic_femtometre(df.baryon_density)
    chemical_potential = (energy_density+pressure)/number_density

    # Interpolate over chemical potential
    interp_array = pqcd_region_dict['mu_array'][
        (min(chemical_potential) < pqcd_region_dict['mu_array']) &
        (max(chemical_potential) > pqcd_region_dict['mu_array'])
    ]
    pressure_interp = np.interp(interp_array, chemical_potential, pressure)
    number_density_interp = np.interp(
        interp_array, chemical_potential, number_density
    )

    inside_region_n = []
    inside_region_p = []
    inside_region_mu = []

    for n, p, mu in zip(
        number_density_interp, pressure_interp, interp_array
    ):
        if (
            pqcd_region_dict['p_boundary_min'] < p
            < pqcd_region_dict['p_boundary_max']
        ):
            min_n = pqcd_region_dict['left_n_boundary'][
                np.argmin(np.abs(pqcd_region_dict['left_p_boundary']-p))
                ]
            max_n = pqcd_region_dict['right_n_boundary'][
                np.argmin(np.abs(pqcd_region_dict['right_p_boundary']-p))
                ]
            if min_n < n < max_n:
                inside_region_n.append(n)
                inside_region_p.append(p)
                inside_region_mu.append(mu)

    # Find the location where the EOS crosses the surface

    # Variable to keep track of the smallest distance between our EOS and the
    # pQCD boundary
    delta = 10

    for n, p, mu in zip(
        inside_region_n, inside_region_p, inside_region_mu
    ):
        for dense_mu, (dense_p_array, dense_n_array) in (
            pqcd_region_dict['dense_arrays'].items()
        ):
            distances = (
                (dense_n_array - n) ** 2 +
                (dense_p_array - p) ** 2 +
                (dense_mu - mu) ** 2
            )
            near_point_index = np.argmin(distances)
            proposed_delta = distances[near_point_index]

            if proposed_delta < delta:
                delta = proposed_delta
                near_point = (
                    dense_n_array[near_point_index],
                    dense_p_array[near_point_index],
                    dense_mu
                )

    mu_intersect.append(near_point[2])

np.savetxt(f'{eos_dir}/mu_intersect.dat', mu_intersect)
