#!/home/eliot.finch/eos/env/bin/python

import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles

from temperance.core.result import EoSPosterior

# eos_posterior = EoSPosterior.from_csv("collated_np_all_post.csv", label="astro")
eos_posterior = EoSPosterior.from_csv('collated_eos.csv', label='astro')

# Marginalised over X
# -------------------

for nterm in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]:

    astro_weight_columns = [
        result.WeightColumn(name=f'weight_{nterm:02}nsat_Xmarg', is_log=False, is_inverted=False)
        ]

    # Pressure vs energy density
    posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'quantiles/p_of_eps_quantiles_{nterm:02}nsat_Xmarg.csv'
        )

    # Pressure vs baryon density
    posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'quantiles/p_of_rho_quantiles_{nterm:02}nsat_Xmarg.csv'
        )

    # Speed of sound vs baryon density
    posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'quantiles/cs2_of_rho_quantiles_{nterm:02}nsat_Xmarg.csv'
        )

    # Mass vs radius
    posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'quantiles/r_of_m_quantiles_{nterm:02}nsat_Xmarg.csv'
        )

    # Lambda vs mass
    posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
        eos_posterior, 
        weight_columns=astro_weight_columns, 
        verbose=True, 
        max_num_samples=80000,
        save_path=f'quantiles/lambda_of_m_quantiles_{nterm:02}nsat_Xmarg.csv'
        )
    
# nterm = nTOV
    
astro_weight_columns = [
    result.WeightColumn(name=f'weight_ntov_Xmarg', is_log=False, is_inverted=False)
    ]

# Pressure vs energy density
posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/p_of_eps_quantiles_ntov_Xmarg.csv'
    )

# Pressure vs baryon density
posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/p_of_rho_quantiles_ntov_Xmarg.csv'
    )

# Speed of sound vs baryon density
posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/cs2_of_rho_quantiles_ntov_Xmarg.csv'
    )

# Mass vs radius
posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/r_of_m_quantiles_ntov_Xmarg.csv'
    )

# Lambda vs mass
posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path=f'quantiles/lambda_of_m_quantiles_ntov_Xmarg.csv'
    )

    # Fixed X

    # for X in [0.5, 2]:

    #     astro_weight_columns = [
    #         result.WeightColumn(name=f'weight_{nterm:02}nsat_X{X}', is_log=False, is_inverted=False)
    #         ]

        # # Pressure vs energy density
        # posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
        #     eos_posterior, 
        #     weight_columns=astro_weight_columns, 
        #     verbose=True, 
        #     max_num_samples=80000,
        #     save_path=f'quantiles/p_of_eps_quantiles_{nterm:02}nsat_X{X}.csv'
        #     )

        # # Pressure vs baryon density
        # posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
        #     eos_posterior, 
        #     weight_columns=astro_weight_columns, 
        #     verbose=True, 
        #     max_num_samples=80000,
        #     save_path=f'quantiles/p_of_rho_quantiles_{nterm:02}nsat_X{X}.csv'
        #     )

        # # Speed of sound vs baryon density
        # posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
        #     eos_posterior, 
        #     weight_columns=astro_weight_columns, 
        #     verbose=True, 
        #     max_num_samples=80000,
        #     save_path=f'quantiles/cs2_of_rho_quantiles_{nterm:02}nsat_X{X}.csv'
        #     )
        
        # Mass vs radius
        # posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
        #     eos_posterior, 
        #     weight_columns=astro_weight_columns, 
        #     verbose=True, 
        #     max_num_samples=80000,
        #     save_path=f'quantiles/r_of_m_quantiles_{nterm:02}nsat_X{X}.csv'
        #     )
        
        # # Lambda vs mass
        # posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
        #     eos_posterior, 
        #     weight_columns=astro_weight_columns, 
        #     verbose=True, 
        #     max_num_samples=80000,
        #     save_path=f'quantiles/lambda_of_m_quantiles_{nterm:02}nsat_X{X}.csv'
        #     )
        