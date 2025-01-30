#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import temperance.core.result as result
import temperance.sampling.eos_prior as eos_prior
import temperance.plotting.get_quantiles as get_quantiles

from temperance.core.result import EoSPosterior

default_eos_prior = eos_prior.EoSPriorSet.get_default()
default_eos_prior.eos_dir = '/home/isaac.legred/local_mrgagn_big_with_cs2c2'
default_eos_prior.macro_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn/'

eos_posterior = EoSPosterior.from_csv(
    '/home/eliot.finch/eos/pqcd/data/eos-draws-default/eos-draws-default.csv',
)

# Marginalised over X
# -------------------

for nterm in [10]:

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
        x_points=np.linspace(5e13, 3e16, 1000),
        save_path=(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
            f'p_of_eps_quantiles_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
        )
    )

    # Speed of sound vs baryon density
    posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
        eos_posterior,
        eos_data=default_eos_prior,
        weight_columns=weight_columns,
        verbose=True,
        max_num_samples=160000,
        x_points=np.linspace(2.8e13, 1.5e16, 1000),
        save_path=(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
            f'cs2_of_rho_quantiles_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
        )
    )

    # Mass vs radius
    posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
        eos_posterior,
        eos_data=default_eos_prior,
        weight_columns=weight_columns,
        verbose=True,
        max_num_samples=160000,
        x_points=np.linspace(0.5, 2.5, 1000),
        save_path=(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
            f'r_of_m_quantiles_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
        )
    )

    # Lambda vs mass
    posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
        eos_posterior,
        eos_data=default_eos_prior,
        weight_columns=weight_columns,
        verbose=True,
        max_num_samples=160000,
        save_path=(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
            f'lambda_of_m_quantiles_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
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

# nterm = nTOV

weight_columns = [
    result.WeightColumn(
        name='pqcd_weight_ntov_Xmarg_mu2.6',
        is_log=False,
        is_inverted=False
    )
]

# Pressure vs energy density
# posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=160000,
#     x_points=np.linspace(5e13, 3e16, 1000),
#     save_path=(
#         '../data/eos-draws-default/quantiles/'
#         'p_of_eps_quantiles_pqcd_ntov_Xmarg_mu2.6.csv'
#     )
# )

# Speed of sound vs baryon density
# posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=160000,
#     x_points=np.linspace(2.8e13, 1.5e16, 1000),
#     save_path=(
#         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#         'cs2_of_rho_quantiles_pqcd_ntov_Xmarg_mu2.6.csv'
#     )
# )

# # Mass vs radius
# posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=160000,
#     x_points=np.linspace(0.5, 2.5, 1000),
#     save_path=(
#         '../data/eos-draws-default/quantiles/'
#         'r_of_m_quantiles_pqcd_ntov_Xmarg_mu2.6.csv'
#     )
# )

# Lambda vs mass
# posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=160000,
#     save_path=(
#         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#         'lambda_of_m_quantiles_pqcd_ntov_Xmarg_mu2.6.csv'
#     )
# )

# # Pressure vs baryon density
# posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
#     eos_posterior,
#     weight_columns=astro_weight_columns,
#     verbose=True,
#     max_num_samples=80000,
#     save_path='../data/quantiles/p_of_rho_quantiles_ntov_Xmarg.csv'
#     )

# Fixed X
# -------

for nterm in [2, 3, 4, 5, 6, 7, 8, 9]:

    for X in [0.5, 2]:

        weight_columns = [
            result.WeightColumn(
                name=f'pqcd_weight_{nterm:02}nsat_X{X}_mu2.6',
                is_log=False,
                is_inverted=False
            )
        ]

        # # Pressure vs energy density
        # posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
        #     eos_posterior,
        #     eos_data=default_eos_prior,
        #     weight_columns=weight_columns,
        #     verbose=True,
        #     max_num_samples=160000,
        #     x_points=np.linspace(5e13, 3e16, 1000),
        #     save_path=(
        #         '../data/eos-draws-default/quantiles/'
        #         f'p_of_eps_quantiles_pqcd_{nterm:02}nsat_X{X}_mu2.6.csv'
        #     )
        # )

        # Speed of sound vs baryon density
        # posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
        #     eos_posterior,
        #     eos_data=default_eos_prior,
        #     weight_columns=weight_columns,
        #     verbose=True,
        #     max_num_samples=160000,
        #     x_points=np.linspace(2.8e13, 1.5e16, 1000),
        #     save_path=(
        #         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
        #         f'cs2_of_rho_quantiles_pqcd_{nterm:02}nsat_X{X}_mu2.6.csv'
        #     )
        # )

        # Mass vs radius
        # posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
        #     eos_posterior,
        #     eos_data=default_eos_prior,
        #     weight_columns=weight_columns,
        #     verbose=True,
        #     max_num_samples=160000,
        #     x_points=np.linspace(0.5, 2.5, 1000),
        #     save_path=(
        #         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
        #         f'r_of_m_quantiles_pqcd_{nterm:02}nsat_X{X}_mu2.6.csv'
        #     )
        # )

        # Lambda vs mass
        # posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
        #     eos_posterior,
        #     eos_data=default_eos_prior,
        #     weight_columns=weight_columns,
        #     verbose=True,
        #     max_num_samples=160000,
        #     save_path=(
        #         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
        #         f'lambda_of_m_quantiles_pqcd_{nterm:02}nsat_X{X}_mu2.6.csv'
        #     )
        # )

        # # Pressure vs baryon density
        # posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
        #     eos_posterior,
        #     weight_columns=astro_weight_columns,
        #     verbose=True,
        #     max_num_samples=80000,
        #     save_path=f'../data/quantiles/p_of_rho_quantiles_{nterm:02}nsat_X{X}.csv'
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

    # # Pressure vs energy density
    # posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    #     eos_posterior,
    #     eos_data=default_eos_prior,
    #     weight_columns=weight_columns,
    #     verbose=True,
    #     max_num_samples=160000,
    #     x_points=np.linspace(5e13, 3e16, 1000),
    #     save_path=(
    #         '../data/eos-draws-default/quantiles/'
    #         f'p_of_eps_quantiles_pqcd_ntov_X{X}_mu2.6.csv'
    #     )
    # )

    # Speed of sound vs baryon density
    # posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    #     eos_posterior,
    #     eos_data=default_eos_prior,
    #     weight_columns=weight_columns,
    #     verbose=True,
    #     max_num_samples=160000,
    #     x_points=np.linspace(2.8e13, 1.5e16, 1000),
    #     save_path=(
    #         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
    #         f'cs2_of_rho_quantiles_pqcd_ntov_X{X}_mu2.6.csv'
    #     )
    # )

    # Mass vs radius
    # posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    #     eos_posterior,
    #     eos_data=default_eos_prior,
    #     weight_columns=weight_columns,
    #     verbose=True,
    #     max_num_samples=160000,
    #     x_points=np.linspace(0.5, 2.5, 1000),
    #     save_path=(
    #         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
    #         f'r_of_m_quantiles_pqcd_ntov_X{X}_mu2.6.csv'
    #     )
    # )

    # Lambda vs mass
    # posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
    #     eos_posterior,
    #     eos_data=default_eos_prior,
    #     weight_columns=weight_columns,
    #     verbose=True,
    #     max_num_samples=160000,
    #     save_path=(
    #         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
    #         f'lambda_of_m_quantiles_pqcd_ntov_X{X}_mu2.6.csv'
    #     )
    # )

    # # Pressure vs baryon density
    # posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
    #     eos_posterior,
    #     weight_columns=astro_weight_columns,
    #     verbose=True,
    #     max_num_samples=80000,
    #     save_path=f'../data/quantiles/p_of_rho_quantiles_ntov_X{X}.csv'
    #     )
