import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles

from temperance.core.result import EoSPosterior
from temperance.sampling.eos_prior import EoSPriorSet

eos_posterior = EoSPosterior.from_csv("collated_np_all_post.csv", label="astro")

astro_weight_columns = [
    result.WeightColumn(name="logweight_total", is_log=True, is_inverted=False)
    ]

posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path='quantiles/p_of_eps_quantiles.csv'
    )
