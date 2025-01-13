#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import temperance.core.result as result
import temperance.sampling.eos_prior as eos_prior
import temperance.plotting.get_quantiles as get_quantiles

from temperance.core.result import EoSPosterior

gp_number = 1
max_num_samples = 33000

default_eos_prior = eos_prior.EoSPriorSet.get_default()
default_eos_prior.eos_dir = (
    '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
    f'gp{gp_number}/margagn'
)
default_eos_prior.macro_dir = (
    '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
    f'gp{gp_number}/margagn'
)
default_eos_prior.macro_path_template = 'macro-eos-draw-%(draw)06d.csv'

eos_posterior = EoSPosterior.from_csv(
    '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
    f'gp{gp_number}/eos-draws-modified-gp{gp_number}.csv',
)

weight_columns = [
    result.WeightColumn(name='prior_weight', is_log=False, is_inverted=False)
]

print('\nPressure vs energy density')

# Pressure vs energy density
posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=max_num_samples,
    x_points=np.linspace(5e13, 3e16, 1000),
    save_path=(
        '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
        f'gp{gp_number}/quantiles/p_of_eps_quantiles_prior.csv'
    )
)

# # Pressure vs baryon density
# posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     verbose=True,
#     max_num_samples=80000,
#     save_path='../data/quantiles/p_of_rho_quantiles.csv'
#     )

print('\nSpeed of sound vs baryon density')

# Speed of sound vs baryon density
posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=max_num_samples,
    x_points=np.linspace(2.8e13, 1.5e16, 1000),
    save_path=(
        '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
        f'gp{gp_number}/quantiles/cs2_of_rho_quantiles_prior.csv'
    )
)

# # Mass vs radius
# posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     verbose=True,
#     max_num_samples=80000,
#     save_path='../data/quantiles/r_of_m_quantiles.csv'
#     )

# # Lambda vs mass
# posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     verbose=True,
#     max_num_samples=80000,
#     save_path='../data/quantiles/lambda_of_m_quantiles.csv'
#     )
