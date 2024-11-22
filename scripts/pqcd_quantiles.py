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

# Marginalised over X
# -------------------

for nterm in [10]:  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]:

    weight_columns = [
        result.WeightColumn(
            name=f'pqcd_weight_{nterm:02}nsat_Xmarg_mu2.6',
            is_log=False,
            is_inverted=False
        )
    ]

    # Pressure vs energy density
    posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
        eos_posterior,
        eos_data=default_eos_prior,
        weight_columns=weight_columns,
        verbose=True,
        max_num_samples=160000,
        x_points=np.linspace(3e13, 2e16, 1000),
        save_path=(
            '../data/eos-draws-default/quantiles/'
            f'p_of_eps_quantiles_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
        )
    )

    # # Pressure vs baryon density
    # posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
    #     eos_posterior,
    #     weight_columns=astro_weight_columns,
    #     verbose=True,
    #     max_num_samples=80000,
    #     save_path=f'../data/quantiles/p_of_rho_quantiles_{nterm:02}nsat_Xmarg.csv'
    #     )

    # # Speed of sound vs baryon density
    # posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    #     eos_posterior,
    #     weight_columns=astro_weight_columns,
    #     verbose=True,
    #     max_num_samples=80000,
    #     save_path=f'../data/quantiles/cs2_of_rho_quantiles_{nterm:02}nsat_Xmarg.csv'
    #     )

    # # Mass vs radius
    # posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    #     eos_posterior,
    #     weight_columns=astro_weight_columns,
    #     verbose=True,
    #     max_num_samples=80000,
    #     save_path=f'../data/quantiles/r_of_m_quantiles_{nterm:02}nsat_Xmarg.csv'
    #     )

    # # Lambda vs mass
    # posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
    #     eos_posterior,
    #     weight_columns=astro_weight_columns,
    #     verbose=True,
    #     max_num_samples=80000,
    #     save_path=f'../data/quantiles/lambda_of_m_quantiles_{nterm:02}nsat_Xmarg.csv'
    #     )

# nterm = nTOV

weight_columns = [
    result.WeightColumn(
        name='pqcd_weight_ntov_Xmarg_mu2.6',
        is_log=False,
        is_inverted=False
    )
]

# Pressure vs energy density
posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=160000,
    x_points=np.linspace(3e13, 2e16, 1000),
    save_path=(
        '../data/eos-draws-default/quantiles/'
        'p_of_eps_quantiles_pqcd_ntov_Xmarg_mu2.6.csv'
    )
)

# # Pressure vs baryon density
# posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     verbose=True,
#     max_num_samples=80000,
#     save_path='../data/quantiles/p_of_rho_quantiles_ntov_Xmarg.csv'
#     )

# # Speed of sound vs baryon density
# posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     verbose=True,
#     max_num_samples=80000,
#     save_path='../data/quantiles/cs2_of_rho_quantiles_ntov_Xmarg.csv'
#     )

# # Mass vs radius
# posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     verbose=True,
#     max_num_samples=80000,
#     save_path='../data/quantiles/r_of_m_quantiles_ntov_Xmarg.csv'
#     )

# # Lambda vs mass
# posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     verbose=True,
#     max_num_samples=80000,
#     save_path='../data/quantiles/lambda_of_m_quantiles_ntov_Xmarg.csv'
#     )

# Fixed X
# -------

for nterm in [10]:  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]:

    for X in [0.5, 2]:

        weight_columns = [
            result.WeightColumn(
                name=f'pqcd_weight_{nterm:02}nsat_X{X}_mu2.6',
                is_log=False,
                is_inverted=False
            )
        ]

        # Pressure vs energy density
        posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
            eos_posterior,
            eos_data=default_eos_prior,
            weight_columns=weight_columns,
            verbose=True,
            max_num_samples=160000,
            x_points=np.linspace(3e13, 2e16, 1000),
            save_path=(
                '../data/eos-draws-default/quantiles/'
                f'p_of_eps_quantiles_pqcd_{nterm:02}nsat_X{X}_mu2.6.csv'
            )
        )

        # # Pressure vs baryon density
        # posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
        #     eos_posterior,
        #     weight_columns=astro_weight_columns,
        #     verbose=True,
        #     max_num_samples=80000,
        #     save_path=f'../data/quantiles/p_of_rho_quantiles_{nterm:02}nsat_X{X}.csv'
        #     )

        # # Speed of sound vs baryon density
        # posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
        #     eos_posterior,
        #     weight_columns=astro_weight_columns,
        #     verbose=True,
        #     max_num_samples=80000,
        #     save_path=f'../data/quantiles/cs2_of_rho_quantiles_{nterm:02}nsat_X{X}.csv'
        #     )

        # # Mass vs radius
        # posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
        #     eos_posterior,
        #     weight_columns=astro_weight_columns,
        #     verbose=True,
        #     max_num_samples=80000,
        #     save_path=f'../data/quantiles/r_of_m_quantiles_{nterm:02}nsat_X{X}.csv'
        #     )

        # # Lambda vs mass
        # posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
        #     eos_posterior,
        #     weight_columns=astro_weight_columns,
        #     verbose=True,
        #     max_num_samples=80000,
        #     save_path=f'../data/quantiles/lambda_of_m_quantiles_{nterm:02}nsat_X{X}.csv'
        #     )

# nterm = nTOV

for X in [0.5, 2]:

    weight_columns = [
        result.WeightColumn(
            name=f'pqcd_weight_ntov_X{X}_mu2.6',
            is_log=False,
            is_inverted=False
        )
    ]

    # Pressure vs energy density
    posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
        eos_posterior,
        eos_data=default_eos_prior,
        weight_columns=weight_columns,
        verbose=True,
        max_num_samples=160000,
        x_points=np.linspace(3e13, 2e16, 1000),
        save_path=(
            '../data/eos-draws-default/quantiles/'
            f'p_of_eps_quantiles_pqcd_ntov_X{X}_mu2.6.csv'
        )
    )

    # # Pressure vs baryon density
    # posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
    #     eos_posterior,
    #     weight_columns=astro_weight_columns,
    #     verbose=True,
    #     max_num_samples=80000,
    #     save_path=f'../data/quantiles/p_of_rho_quantiles_ntov_X{X}.csv'
    #     )

    # # Speed of sound vs baryon density
    # posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    #     eos_posterior,
    #     weight_columns=astro_weight_columns,
    #     verbose=True,
    #     max_num_samples=80000,
    #     save_path=f'../data/quantiles/cs2_of_rho_quantiles_ntov_X{X}.csv'
    #     )

    # # Mass vs radius
    # posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    #     eos_posterior,
    #     weight_columns=astro_weight_columns,
    #     verbose=True,
    #     max_num_samples=80000,
    #     save_path=f'../data/quantiles/r_of_m_quantiles_ntov_X{X}.csv'
    #     )

    # # Lambda vs mass
    # posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
    #     eos_posterior,
    #     weight_columns=astro_weight_columns,
    #     verbose=True,
    #     max_num_samples=80000,
    #     save_path=f'../data/quantiles/lambda_of_m_quantiles_ntov_X{X}.csv'
    #     )
