#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles
import temperance.sampling.eos_prior as eos_prior

from temperance.core.result import EoSPosterior

max_num_samples = 70000

default_eos_prior = eos_prior.EoSPriorSet.get_default()
default_eos_prior.eos_dir = '/home/isaac.legred/local_mrgagn_big_with_cs2c2'
default_eos_prior.macro_dir = '/home/philippe.landry/nseos/eos/gp/mrgagn/'

eos_posterior = EoSPosterior.from_csv(
    '../data/eos-draws-default/eos-draws-default-with-J0437-nonzero-astro-alt-xray.csv',
)

# Astro only
# ----------

print('Computing astro-only quantiles...')

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
    max_num_samples=max_num_samples,
    x_points=np.linspace(5e13, 3e16, 1000),
    save_path=(
        '../data/eos-draws-default/quantiles/'
        'p_of_eps_quantiles_astro-alt-xray.csv'
    )
)

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
        '../data/eos-draws-default/quantiles/'
        'cs2_of_rho_quantiles_astro-alt-xray.csv'
    )
)

print('\nMass vs radius')

# Mass vs radius
posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=max_num_samples,
    x_points=np.linspace(0.5, 2.5, 1000),
    save_path='../data/eos-draws-default/quantiles/r_of_m_quantiles_astro-alt-xray.csv'
)

# Astro + pQCD (max)
# ------------------

# 10nsat

print('Computing astro+pQCD (max, 10nsat) quantiles...')

weight_columns = [
    result.WeightColumn(
        name='logweight_total',
        is_log=True,
        is_inverted=False
    ),
    result.WeightColumn(
        name='pqcd_weight_10nsat_Xmarg_mu2.6',
        is_log=False,
        is_inverted=False
    ),
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
        '../data/eos-draws-default/quantiles/'
        'p_of_eps_quantiles_astro_pqcd_10nsat_Xmarg_mu2.6-alt-xray.csv'
    )
)

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
        '../data/eos-draws-default/quantiles/'
        'cs2_of_rho_quantiles_astro_pqcd_10nsat_Xmarg_mu2.6-alt-xray.csv'
    )
)

print('\nMass vs radius')

# Mass vs radius
posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=max_num_samples,
    x_points=np.linspace(0.5, 2.5, 1000),
    save_path=(
        '../data/eos-draws-default/quantiles/'
        'r_of_m_quantiles_astro_pqcd_10nsat_Xmarg_mu2.6-alt-xray.csv'
    )
)

# ntov

print('Computing astro+pQCD (max, ntov) quantiles...')

weight_columns = [
    result.WeightColumn(
        name='logweight_total',
        is_log=True,
        is_inverted=False
    ),
    result.WeightColumn(
        name='pqcd_weight_ntov_Xmarg_mu2.6',
        is_log=False,
        is_inverted=False
    ),
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
        '../data/eos-draws-default/quantiles/'
        'p_of_eps_quantiles_astro_pqcd_ntov_Xmarg_mu2.6-alt-xray.csv'
    )
)

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
        '../data/eos-draws-default/quantiles/'
        'cs2_of_rho_quantiles_astro_pqcd_ntov_Xmarg_mu2.6-alt-xray.csv'
    )
)

print('\nMass vs radius')

# Mass vs radius
posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=max_num_samples,
    x_points=np.linspace(0.5, 2.5, 1000),
    save_path=(
        '../data/eos-draws-default/quantiles/'
        'r_of_m_quantiles_astro_pqcd_ntov_Xmarg_mu2.6-alt-xray.csv'
    )
)

# Astro + pQCD (marg)
# ------------------

# 10nsat

print('Computing astro+pQCD (marg, 10nsat) quantiles...')

weight_columns = [
    result.WeightColumn(
        name='logweight_total',
        is_log=True,
        is_inverted=False
    ),
    result.WeightColumn(
        name='pqcd_weight_10nsat_marg',
        is_log=False,
        is_inverted=False
    ),
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
        '../data/eos-draws-default/quantiles/'
        'p_of_eps_quantiles_astro_pqcd_10nsat_marg-alt-xray.csv'
    )
)

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
        '../data/eos-draws-default/quantiles/'
        'cs2_of_rho_quantiles_astro_pqcd_10nsat_marg-alt-xray.csv'
    )
)

print('\nMass vs radius')

# Mass vs radius
posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=max_num_samples,
    x_points=np.linspace(0.5, 2.5, 1000),
    save_path=(
        '../data/eos-draws-default/quantiles/'
        'r_of_m_quantiles_astro_pqcd_10nsat_marg-alt-xray.csv'
    )
)

# ntov

print('Computing astro+pQCD (marg, ntov) quantiles...')

weight_columns = [
    result.WeightColumn(
        name='logweight_total',
        is_log=True,
        is_inverted=False
    ),
    result.WeightColumn(
        name='pqcd_weight_ntov_marg',
        is_log=False,
        is_inverted=False
    ),
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
        '../data/eos-draws-default/quantiles/'
        'p_of_eps_quantiles_astro_pqcd_ntov_marg-alt-xray.csv'
    )
)

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
        '../data/eos-draws-default/quantiles/'
        'cs2_of_rho_quantiles_astro_pqcd_ntov_marg-alt-xray.csv'
    )
)

print('\nMass vs radius')

# Mass vs radius
posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    eos_posterior,
    eos_data=default_eos_prior,
    weight_columns=weight_columns,
    verbose=True,
    max_num_samples=max_num_samples,
    x_points=np.linspace(0.5, 2.5, 1000),
    save_path=(
        '../data/eos-draws-default/quantiles/'
        'r_of_m_quantiles_astro_pqcd_ntov_marg-alt-xray.csv'
    )
)
