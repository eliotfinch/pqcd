import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles
import temperance.sampling.eos_prior as eos_prior

from temperance.core.result import EoSPosterior

eos_posterior = EoSPosterior.from_csv(
    '../data/eos-draws-modified-12.csv',
    label='astro'
    )

default_eos_prior = eos_prior.EoSPriorSet.get_default()
default_eos_prior.eos_dir = (
    '/Users/eliot/Documents/Research/EOS/pqcd/data/eos-draws-modified/'
    '12/margagn'
)
default_eos_prior.macro_dir = (
    '/Users/eliot/Documents/Research/EOS/pqcd/data/eos-draws-modified/'
    '12/margagn'
)
default_eos_prior.macro_path_template = 'macro-eos-draw-%(draw)06d.csv'

astro_weight_columns = [
    result.WeightColumn(name='logweight_total', is_log=True, is_inverted=False)
]

# Pressure vs energy density
posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior,
    weight_columns=astro_weight_columns,
    eos_data=default_eos_prior,
    verbose=True,
    max_num_samples=6300,
    save_path='../data/eos-draws-modified/12/quantiles/p_of_eps_quantiles.csv'
)

# Pressure vs baryon density
posterior_quantiles = get_quantiles.get_p_of_rho_quantiles(
    eos_posterior,
    weight_columns=astro_weight_columns,
    eos_data=default_eos_prior,
    verbose=True,
    max_num_samples=6300,
    save_path='../data/eos-draws-modified/12/quantiles/p_of_rho_quantiles.csv'
)

# Speed of sound vs baryon density
posterior_quantiles = get_quantiles.get_cs2_of_rho_quantiles(
    eos_posterior,
    weight_columns=astro_weight_columns,
    eos_data=default_eos_prior,
    verbose=True,
    max_num_samples=6300,
    save_path=(
        '../data/eos-draws-modified/12/quantiles/cs2_of_rho_quantiles.csv'
    )
)

# Mass vs radius
posterior_quantiles = get_quantiles.get_r_of_m_quantiles(
    eos_posterior,
    weight_columns=astro_weight_columns,
    eos_data=default_eos_prior,
    verbose=True,
    max_num_samples=6300,
    save_path='../data/eos-draws-modified/12/quantiles/r_of_m_quantiles.csv'
)

# Lambda vs mass
posterior_quantiles = get_quantiles.get_lambda_of_m_quantiles(
    eos_posterior,
    weight_columns=astro_weight_columns,
    eos_data=default_eos_prior,
    verbose=True,
    max_num_samples=6300,
    save_path=(
        '../data/eos-draws-modified/12/quantiles/lambda_of_m_quantiles.csv'
    )
)
