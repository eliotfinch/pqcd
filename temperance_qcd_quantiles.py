#!/home/eliot.finch/eos/env/bin/python

import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles

from temperance.core.result import EoSPosterior

# eos_posterior = EoSPosterior.from_csv("collated_np_all_post.csv", label="astro")
eos_posterior = EoSPosterior.from_csv('collated_eos.csv', label='astro')

for ns in [5, 6, 7, 8, 9, 10]:

    # Marginalised over X

    # astro_weight_columns = [
    #     result.WeightColumn(name=f'weight_ns{ns:02}_Xmarg', is_log=False, is_inverted=False)
    #     ]

    # # Pressure vs energy density
    # posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    #     eos_posterior, 
    #     weight_columns=astro_weight_columns, 
    #     verbose=True, 
    #     max_num_samples=80000,
    #     save_path=f'quantiles/p_of_eps_quantiles_ns{ns:02}_Xmarg.csv'
    #     )

    # # Pressure vs baryon density
    # posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
    #     eos_posterior, 
    #     weight_columns=astro_weight_columns, 
    #     verbose=True, 
    #     max_num_samples=80000,
    #     save_path=f'quantiles/p_of_rho_quantiles_ns{ns:02}_Xmarg.csv'
    #     )

    # # Speed of sound vs baryon density
    # posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    #     eos_posterior, 
    #     weight_columns=astro_weight_columns, 
    #     verbose=True, 
    #     max_num_samples=80000,
    #     save_path=f'quantiles/cs2_of_rho_quantiles_ns{ns:02}_Xmarg.csv'
    #     )

    # # Mass vs radius
    # posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    #     eos_posterior, 
    #     weight_columns=astro_weight_columns, 
    #     verbose=True, 
    #     max_num_samples=80000,
    #     save_path=f'quantiles/r_of_m_quantiles_ns{ns:02}_Xmarg.csv'
    #     )

    # # Lambda vs mass
    # posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
    #     eos_posterior, 
    #     weight_columns=astro_weight_columns, 
    #     verbose=True, 
    #     max_num_samples=80000,
    #     save_path=f'quantiles/lambda_of_m_quantiles_ns{ns:02}_Xmarg.csv'
    #     )

    # Fixed X

    for X in [0.5, 2]:

        astro_weight_columns = [
            result.WeightColumn(name=f'weight_ns{ns:02}_X{X}', is_log=False, is_inverted=False)
            ]

        # Pressure vs energy density
        posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
            eos_posterior, 
            weight_columns=astro_weight_columns, 
            verbose=True, 
            max_num_samples=80000,
            save_path=f'quantiles/p_of_eps_quantiles_ns{ns:02}_X{X}.csv'
            )

        # Pressure vs baryon density
        posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
            eos_posterior, 
            weight_columns=astro_weight_columns, 
            verbose=True, 
            max_num_samples=80000,
            save_path=f'quantiles/p_of_rho_quantiles_ns{ns:02}_X{X}.csv'
            )

        # Speed of sound vs baryon density
        posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
            eos_posterior, 
            weight_columns=astro_weight_columns, 
            verbose=True, 
            max_num_samples=80000,
            save_path=f'quantiles/cs2_of_rho_quantiles_ns{ns:02}_X{X}.csv'
            )