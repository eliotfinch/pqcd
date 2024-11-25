#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles
import temperance.sampling.eos_prior as eos_prior

from temperance.core.result import EoSPosterior

set_number = 24

default_eos_prior = eos_prior.EoSPriorSet.get_default()
default_eos_prior.eos_dir = (
    '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
    f'{set_number:02}/margagn'
)
default_eos_prior.macro_dir = (
    '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
    f'{set_number:02}/margagn'
)
default_eos_prior.macro_path_template = 'macro-eos-draw-%(draw)06d.csv'

eos_posterior = EoSPosterior.from_csv(
    f'../data/eos-draws-modified/eos-draws-modified-{set_number:02}.csv',
)


weight_columns = [
    result.WeightColumn(name='logweight_total', is_log=True, is_inverted=False)
]

print('\nPressure vs energy density')

# Pressure vs energy density
posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=16000,
    x_points=np.linspace(3e13, 2e16, 1000),
    save_path=(
        f'../data/eos-draws-modified/{set_number:02}/quantiles/'
        'p_of_eps_astro_quantiles.csv'
    )
)

# print('\nPressure vs baryon density')

# # Pressure vs baryon density
# posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     eos_data=default_eos_prior,
#     verbose=True,
#     max_num_samples=16000,
#     save_path='../data/eos-draws-modified/12/quantiles/p_of_rho_quantiles.csv'
# )

print('\nSpeed of sound vs baryon density')

# Speed of sound vs baryon density
posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=16000,
    x_points=np.linspace(2.8e13, 2.8e15, 1000),
    save_path=(
        f'../data/eos-draws-modified/{set_number:02}/quantiles/'
        'cs2_of_rho_astro_quantiles.csv'
    )
)

# print('\nMass vs radius')

# # Mass vs radius
# posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     eos_data=default_eos_prior,
#     verbose=True,
#     max_num_samples=6300,
#     save_path='../data/eos-draws-modified/12/quantiles/r_of_m_quantiles.csv'
# )

# print('\nLambda vs mass')

# # Lambda vs mass
# posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     eos_data=default_eos_prior,
#     verbose=True,
#     max_num_samples=6300,
#     save_path=(
#         '../data/eos-draws-modified/12/quantiles/lambda_of_m_quantiles.csv'
#     )
# )
