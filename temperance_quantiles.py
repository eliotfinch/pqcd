#!/home/eliot.finch/eos/env/bin/python

import temperance.core.result as result
import temperance.plotting.get_quantiles as get_quantiles

from temperance.core.result import EoSPosterior

# eos_posterior = EoSPosterior.from_csv("collated_np_all_post.csv", label="astro")
eos_posterior = EoSPosterior.from_csv('collated_eos.csv', label='astro')

# astro_weight_columns = [
#     result.WeightColumn(name='logweight_total', is_log=True, is_inverted=False)
#     ]
astro_weight_columns = [
    result.WeightColumn(name='weight_ns10_Xmarg', is_log=False, is_inverted=False)
    ]

posterior_quantiles = get_quantiles.get_p_of_eps_quantiles(
    eos_posterior, 
    weight_columns=astro_weight_columns, 
    verbose=True, 
    max_num_samples=80000,
    save_path='quantiles/p_of_eps_quantiles_ns10_Xmarg.csv'
    )
