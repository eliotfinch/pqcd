#!/home/eliot.finch/eos/env/bin/python

import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles

from temperance.core.result import EoSPosterior

# eos_posterior = EoSPosterior.from_csv("collated_np_all_post.csv", label="astro")
eos_posterior = EoSPosterior.from_csv('collated_eos.csv', label='astro')

astro_weight_columns = [
    result.WeightColumn(name='logweight_total', is_log=True, is_inverted=False)
    ]

# Pressure vs energy density
posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/p_of_eps_quantiles.csv'
    )

# Pressure vs baryon density
posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/p_of_rho_quantiles.csv'
    )

# Speed of sound vs baryon density
posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/cs2_of_rho_quantiles.csv'
    )

# Mass vs radius
posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/r_of_m_quantiles.csv'
    )

# Lambda vs mass
posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/lambda_of_m_quantiles.csv'
    )