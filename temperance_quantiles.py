import temperance.core.result as result
from temperance.core.result import EoSPosterior

from temperance.sampling.eos_prior import EoSPriorSet

import temperance.plotting.get_quantiles as get_quantiles
if  __name__ == "__main__":
    eos_posterior = EoSPosterior.from_csv("collated_np_all_post.csv", label="astro")
    #prior_quantiles=  tmplot.get_quantiles.get_quantiles(eos_posterior, weight_columns=[])
    astro_weight_columns = [result.WeightColumn(
        name="logweight_total", is_log=True,
        is_inverted=False)]
    posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
        eos_posterior,
        weight_columns=astro_weight_columns, verbose=True, save_path='quantiles.csv')
    print(eos_posterior.weight_columns_available)
    print(eos_posterior.samples)
    default_eos_prior = EoSPriorSet.get_default()
