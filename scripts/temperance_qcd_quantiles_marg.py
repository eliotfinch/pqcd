#!/home/eliot.finch/eos/env/bin/python

import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles

from temperance.core.result import EoSPosterior

# eos_posterior = EoSPosterior.from_csv("collated_np_all_post.csv", label="astro")
eos_posterior = EoSPosterior.from_csv('../data/eos-draws-default.csv', label='astro')

for nterm in [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]:

    astro_weight_columns = [
        result.WeightColumn(name=f'weight_{nterm:02}nsat_marg', is_log=False, is_inverted=False)
        ]

    # Pressure vs energy density
    posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'../data/quantiles/p_of_eps_quantiles_{nterm:02}nsat_marg.csv'
        )

    # Pressure vs baryon density
    posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'../data/quantiles/p_of_rho_quantiles_{nterm:02}nsat_Xmarg.csv'
        )

    # Speed of sound vs baryon density
    posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'../data/quantiles/cs2_of_rho_quantiles_{nterm:02}nsat_marg.csv'
        )

    # Mass vs radius
    posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'../data/quantiles/r_of_m_quantiles_{nterm:02}nsat_marg.csv'
        )

    # Lambda vs mass
    posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'../data/quantiles/lambda_of_m_quantiles_{nterm:02}nsat_marg.csv'
        )
    
# nterm = nTOV
    
astro_weight_columns = [
    result.WeightColumn(name=f'weight_ntov_marg', is_log=False, is_inverted=False)
    ]

# Pressure vs energy density
posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'../data/quantiles/p_of_eps_quantiles_ntov_marg.csv'
    )

# Pressure vs baryon density
posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'../data/quantiles/p_of_rho_quantiles_ntov_marg.csv'
    )

# Speed of sound vs baryon density
posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'../data/quantiles/cs2_of_rho_quantiles_ntov_marg.csv'
    )

# Mass vs radius
posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'../data/quantiles/r_of_m_quantiles_ntov_marg.csv'
    )

# Lambda vs mass
posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'../data/quantiles/lambda_of_m_quantiles_ntov_marg.csv'
    )