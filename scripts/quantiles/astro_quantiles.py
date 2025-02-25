#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles
import temperance.sampling.eos_prior as eos_prior

from temperance.core.result import EoSPosterior

max_num_samples = 10000  # 70000

default_eos_prior = eos_prior.EoSPriorSet.get_default()
default_eos_prior.eos_dir = '/home/isaac.legred/local_mrgagn_big_with_cs2c2'
default_eos_prior.macro_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn/'

eos_posterior = EoSPosterior.from_csv(
    '/home/eliot.finch/eos/pqcd/data/eos-draws-default/'
    'eos-draws-default-nonzero-astro.csv',
)

# Radio only
# ----------

print('Computing radio-only quantiles...', flush=True)

weight_columns = [
    result.WeightColumn(
        name='logweight_Fonseca_J0740',
        is_log=True,
        is_inverted=False
    ),
    result.WeightColumn(
        name='logweight_Antoniadis_J0348',
        is_log=True,
        is_inverted=False
    ),
]

print('\nPressure vs energy density', flush=True)

# Pressure vs energy density
posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=max_num_samples,
    x_points=np.linspace(5e13, 3e16, 1000),
    save_path=(
        '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
        'p_of_eps_quantiles_radio_reduced.csv'
    )
)

print('\nSpeed of sound vs baryon density', flush=True)

# Speed of sound vs baryon density
posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=max_num_samples,
    x_points=np.linspace(2.8e13, 1.5e16, 1000),
    save_path=(
        '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
        'cs2_of_rho_quantiles_radio_reduced.csv'
    )
)

# Radio + pQCD (max)
# ------------------

for nterm in [2, 4, 6, 8, 10]:

    print(
        f'Computing radio + pQCD (max, {nterm:02}nsat) quantiles...',
        flush=True
    )

    weight_columns = [
        result.WeightColumn(
            name='logweight_Fonseca_J0740',
            is_log=True,
            is_inverted=False
        ),
        result.WeightColumn(
            name='logweight_Antoniadis_J0348',
            is_log=True,
            is_inverted=False
        ),
        result.WeightColumn(
            name=f'pqcd_weight_{nterm:02}nsat_Xmarg_mu2.6',
            is_log=False,
            is_inverted=False
        ),
    ]

    print('\nPressure vs energy density', flush=True)

    # Pressure vs energy density
    posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
        eos_posterior,
        eos_data=default_eos_prior,
        weight_columns=weight_columns,
        verbose=True,
        max_num_samples=max_num_samples,
        x_points=np.linspace(5e13, 3e16, 1000),
        save_path=(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
            f'p_of_eps_quantiles_radio_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
        )
    )

    print('\nSpeed of sound vs baryon density', flush=True)

    # Speed of sound vs baryon density
    posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
        eos_posterior,
        eos_data=default_eos_prior,
        weight_columns=weight_columns,
        verbose=True,
        max_num_samples=max_num_samples,
        x_points=np.linspace(2.8e13, 1.5e16, 1000),
        save_path=(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
            f'cs2_of_rho_quantiles_radio_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
        )
    )

# Radio + pQCD (max, nTOV)
# ------------------------

# print('Computing radio + pQCD (max, ntov) quantiles...', flush=True)

# weight_columns = [
#     result.WeightColumn(
#         name='logweight_Fonseca_J0740',
#         is_log=True,
#         is_inverted=False
#     ),
#     result.WeightColumn(
#         name='logweight_Antoniadis_J0348',
#         is_log=True,
#         is_inverted=False
#     ),
#     result.WeightColumn(
#         name='pqcd_weight_ntov_Xmarg_mu2.6',
#         is_log=False,
#         is_inverted=False
#     ),
# ]

# print('\nPressure vs energy density')

# # Pressure vs energy density
# posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(5e13, 3e16, 1000),
#     save_path=(
#         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#         'p_of_eps_quantiles_radio_pqcd_ntov_Xmarg_mu2.6.csv'
#     )
# )

# print('\nSpeed of sound vs baryon density')

# # Speed of sound vs baryon density
# posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(2.8e13, 1.5e16, 1000),
#     save_path=(
#         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#         'cs2_of_rho_quantiles_radio_pqcd_ntov_Xmarg_mu2.6.csv'
#     )
# )

# Radio + pQCD (marg)
# -------------------

for nterm in [2, 4, 6, 8, 10]:

    print(
        f'Computing radio + pQCD (marg, {nterm:02}nsat) quantiles...',
        flush=True
    )

    weight_columns = [
        result.WeightColumn(
            name='logweight_Fonseca_J0740',
            is_log=True,
            is_inverted=False
        ),
        result.WeightColumn(
            name='logweight_Antoniadis_J0348',
            is_log=True,
            is_inverted=False
        ),
        result.WeightColumn(
            name=f'pqcd_weight_{nterm:02}nsat_marg',
            is_log=False,
            is_inverted=False
        ),
    ]

    print('\nPressure vs energy density', flush=True)

    # Pressure vs energy density
    posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
        eos_posterior,
        eos_data=default_eos_prior,
        weight_columns=weight_columns,
        verbose=True,
        max_num_samples=max_num_samples,
        x_points=np.linspace(5e13, 3e16, 1000),
        save_path=(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
            f'p_of_eps_quantiles_radio_pqcd_{nterm:02}nsat_marg.csv'
        )
    )

    print('\nSpeed of sound vs baryon density', flush=True)

    # Speed of sound vs baryon density
    posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
        eos_posterior,
        eos_data=default_eos_prior,
        weight_columns=weight_columns,
        verbose=True,
        max_num_samples=max_num_samples,
        x_points=np.linspace(2.8e13, 1.5e16, 1000),
        save_path=(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
            f'cs2_of_rho_quantiles_radio_pqcd_{nterm:02}nsat_marg.csv'
        )
    )

# Radio + pQCD (marg, nTOV)
# -------------------------

# print('Computing radio + pQCD (marg, ntov) quantiles...')

# weight_columns = [
#     result.WeightColumn(
#         name='logweight_Fonseca_J0740',
#         is_log=True,
#         is_inverted=False
#     ),
#     result.WeightColumn(
#         name='logweight_Antoniadis_J0348',
#         is_log=True,
#         is_inverted=False
#     ),
#     result.WeightColumn(
#         name='pqcd_weight_ntov_marg',
#         is_log=False,
#         is_inverted=False
#     ),
# ]

# print('\nPressure vs energy density')

# # Pressure vs energy density
# posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(5e13, 3e16, 1000),
#     save_path=(
#         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#         'p_of_eps_quantiles_radio_pqcd_ntov_marg.csv'
#     )
# )

# print('\nSpeed of sound vs baryon density')

# # Speed of sound vs baryon density
# posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(2.8e13, 1.5e16, 1000),
#     save_path=(
#         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#         'cs2_of_rho_quantiles_astro_pqcd_ntov_marg.csv'
#     )
# )

# Astro only
# ----------

# print('Computing astro-only quantiles...')

# weight_columns = [
#     result.WeightColumn(
#         name='logweight_total',
#         is_log=True,
#         is_inverted=False
#     )
# ]

# print('\nPressure vs energy density')

# # Pressure vs energy density
# posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(5e13, 3e16, 1000),
#     save_path=(
#         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#         'p_of_eps_quantiles_astro.csv'
#     )
# )

# print('\nSpeed of sound vs baryon density')

# # Speed of sound vs baryon density
# posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(2.8e13, 1.5e16, 1000),
#     save_path=(
#         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#         'cs2_of_rho_quantiles_astro.csv'
#     )
# )

# print('\nMass vs radius')

# # Mass vs radius
# posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(0.5, 2.5, 1000),
#     save_path=(
#         '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#         'r_of_m_quantiles_astro.csv'
#     )
# )

# Astro + pQCD (max)
# ------------------

# for nterm in [2, 3, 4, 5, 6, 7, 8, 9]:

#     print(
#         f'Computing astro+pQCD (max, {nterm:02}nsat) quantiles...',
#         flush=True
#     )

#     weight_columns = [
#         result.WeightColumn(
#             name='logweight_total',
#             is_log=True,
#             is_inverted=False
#         ),
#         result.WeightColumn(
#             name=f'pqcd_weight_{nterm:02}nsat_Xmarg_mu2.6',
#             is_log=False,
#             is_inverted=False
#         ),
#     ]

#     print('\nPressure vs energy density', flush=True)

#     # Pressure vs energy density
#     posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
#         eos_posterior,
#         eos_data=default_eos_prior,
#         weight_columns=weight_columns,
#         verbose=True,
#         max_num_samples=max_num_samples,
#         x_points=np.linspace(5e13, 3e16, 1000),
#         save_path=(
#             '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#             f'p_of_eps_quantiles_astro_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
#         )
#     )

#     print('\nSpeed of sound vs baryon density', flush=True)

#     # Speed of sound vs baryon density
#     posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
#         eos_posterior,
#         eos_data=default_eos_prior,
#         weight_columns=weight_columns,
#         verbose=True,
#         max_num_samples=max_num_samples,
#         x_points=np.linspace(2.8e13, 1.5e16, 1000),
#         save_path=(
#             '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#             f'cs2_of_rho_quantiles_astro_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
#         )
#     )

#     print('\nMass vs radius', flush=True)

#     # Mass vs radius
#     posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#         eos_posterior,
#         eos_data=default_eos_prior,
#         weight_columns=weight_columns,
#         verbose=True,
#         max_num_samples=max_num_samples,
#         x_points=np.linspace(0.5, 2.5, 1000),
#         save_path=(
#             '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#             f'r_of_m_quantiles_astro_pqcd_{nterm:02}nsat_Xmarg_mu2.6.csv'
#         )
#     )

# ntov

# print('Computing astro+pQCD (max, ntov) quantiles...')

# weight_columns = [
#     result.WeightColumn(
#         name='logweight_total',
#         is_log=True,
#         is_inverted=False
#     ),
#     result.WeightColumn(
#         name='pqcd_weight_ntov_Xmarg_mu2.6',
#         is_log=False,
#         is_inverted=False
#     ),
# ]

# print('\nPressure vs energy density')

# # Pressure vs energy density
# posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(5e13, 3e16, 1000),
#     save_path=(
#         '../data/eos-draws-default/quantiles/'
#         'p_of_eps_quantiles_astro_pqcd_ntov_Xmarg_mu2.6-alt-xray.csv'
#     )
# )

# print('\nSpeed of sound vs baryon density')

# # Speed of sound vs baryon density
# posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(2.8e13, 1.5e16, 1000),
#     save_path=(
#         '../data/eos-draws-default/quantiles/'
#         'cs2_of_rho_quantiles_astro_pqcd_ntov_Xmarg_mu2.6-alt-xray.csv'
#     )
# )

# print('\nMass vs radius')

# # Mass vs radius
# posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(0.5, 2.5, 1000),
#     save_path=(
#         '../data/eos-draws-default/quantiles/'
#         'r_of_m_quantiles_astro_pqcd_ntov_Xmarg_mu2.6-alt-xray.csv'
#     )
# )

# Astro + pQCD (marg)
# ------------------

# for nterm in [2, 3, 4, 5, 6, 7, 8, 9]:

#     print(
#         f'Computing astro+pQCD (marg, {nterm:02}nsat) quantiles...',
#         flush=True
#     )

#     weight_columns = [
#         result.WeightColumn(
#             name='logweight_total',
#             is_log=True,
#             is_inverted=False
#         ),
#         result.WeightColumn(
#             name=f'pqcd_weight_{nterm:02}nsat_marg',
#             is_log=False,
#             is_inverted=False
#         ),
#     ]

#     print('\nPressure vs energy density', flush=True)

#     # Pressure vs energy density
#     posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
#         eos_posterior,
#         eos_data=default_eos_prior,
#         weight_columns=weight_columns,
#         verbose=True,
#         max_num_samples=max_num_samples,
#         x_points=np.linspace(5e13, 3e16, 1000),
#         save_path=(
#             '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#             f'p_of_eps_quantiles_astro_pqcd_{nterm:02}nsat_marg.csv'
#         )
#     )

#     print('\nSpeed of sound vs baryon density', flush=True)

#     # Speed of sound vs baryon density
#     posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
#         eos_posterior,
#         eos_data=default_eos_prior,
#         weight_columns=weight_columns,
#         verbose=True,
#         max_num_samples=max_num_samples,
#         x_points=np.linspace(2.8e13, 1.5e16, 1000),
#         save_path=(
#             '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#             f'cs2_of_rho_quantiles_astro_pqcd_{nterm:02}nsat_marg.csv'
#         )
#     )

#     print('\nMass vs radius', flush=True)

#     # Mass vs radius
#     posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#         eos_posterior,
#         eos_data=default_eos_prior,
#         weight_columns=weight_columns,
#         verbose=True,
#         max_num_samples=max_num_samples,
#         x_points=np.linspace(0.5, 2.5, 1000),
#         save_path=(
#             '/home/eliot.finch/eos/pqcd/data/eos-draws-default/quantiles/'
#             f'r_of_m_quantiles_astro_pqcd_{nterm:02}nsat_marg.csv'
#         )
#     )

# ntov

# print('Computing astro+pQCD (marg, ntov) quantiles...')

# weight_columns = [
#     result.WeightColumn(
#         name='logweight_total',
#         is_log=True,
#         is_inverted=False
#     ),
#     result.WeightColumn(
#         name='pqcd_weight_ntov_marg',
#         is_log=False,
#         is_inverted=False
#     ),
# ]

# print('\nPressure vs energy density')

# # Pressure vs energy density
# posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(5e13, 3e16, 1000),
#     save_path=(
#         '../data/eos-draws-default/quantiles/'
#         'p_of_eps_quantiles_astro_pqcd_ntov_marg-alt-xray.csv'
#     )
# )

# print('\nSpeed of sound vs baryon density')

# # Speed of sound vs baryon density
# posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(2.8e13, 1.5e16, 1000),
#     save_path=(
#         '../data/eos-draws-default/quantiles/'
#         'cs2_of_rho_quantiles_astro_pqcd_ntov_marg-alt-xray.csv'
#     )
# )

# print('\nMass vs radius')

# # Mass vs radius
# posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
#     eos_posterior,
#     eos_data=default_eos_prior,
#     weight_columns=weight_columns,
#     verbose=True,
#     max_num_samples=max_num_samples,
#     x_points=np.linspace(0.5, 2.5, 1000),
#     save_path=(
#         '../data/eos-draws-default/quantiles/'
#         'r_of_m_quantiles_astro_pqcd_ntov_marg-alt-xray.csv'
#     )
# )
