#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import temperance.core.result as result
import temperance.sampling.eos_prior as eos_prior
import temperance.plotting.get_quantiles as get_quantiles

from temperance.core.result import EoSPosterior

default_eos_prior = eos_prior.EoSPriorSet.get_default()
default_eos_prior.eos_dir = '/home/isaac.legred/local_mrgagn_big_with_cs2c2'
default_eos_prior.macro_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn/'

# All draws
eos_posterior = EoSPosterior.from_csv(
    '../data/eos-draws-default/collated_np_all_post_edit.csv',
)

weight_columns = [
    result.WeightColumn(name='prior_weight', is_log=False, is_inverted=False)
]

# Pressure vs energy density
posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=160000,
    x_points=np.linspace(5e13, 3e16, 1000),
    save_path=(
        '../data/eos-draws-default/quantiles/p_of_eps_quantiles_prior.csv'
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

# Speed of sound vs baryon density
posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=160000,
    x_points=np.linspace(2.8e13, 1.5e16, 1000),
    save_path=(
        '../data/eos-draws-default/quantiles/cs2_of_rho_quantiles_prior.csv'
    )
)

# # Mass vs radius
# posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=160000,
#     x_points=np.linspace(0.5, 2.5, 1000),
#     save_path='../data/eos-draws-default/r_of_m_quantiles_prior.csv'
#     )

# # Lambda vs mass
# posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     verbose=True,
#     max_num_samples=80000,
#     save_path='../data/quantiles/lambda_of_m_quantiles.csv'
#     )
