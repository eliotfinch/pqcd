import temperance.core.result as result
from temperance.weighing import weigh_by_density_estimate
from temperance.sampling import eos_prior
from temperance.core.result import EoSPosterior

from tqdm import tqdm
import pandas as pd
import numpy as np


class FlatMassPrior:
    def __init__(self, m_min, m_max, seed=None):
        self.m_min = m_min
        self.m_max = m_max
        self.rng = np.random.default_rng(seed)

    def sample(self, size):
        return self.rng.uniform(self.m_min, self.m_max, size)


def marginalize_over_mr_samples(
    mr_samples, num_marginalization_samples=50, nicer_tag="j0740"
):
    marginalizable_samples = mr_samples[["eos", "Mmax", f"logweight_{nicer_tag}"]]
    marginalizable_samples[f"weight_{nicer_tag}"] = np.exp(
        marginalizable_samples[f"logweight_{nicer_tag}"]
    )
    marginalized_weights = marginalizable_samples.groupby("eos").mean()
    marginalized_weights.reset_index(inplace=True)
    marginalized_weights[f"logweight_{nicer_tag}"] = np.log(marginalized_weights[f"weight_{nicer_tag}"])
    return marginalized_weights

def weigh_eoss_by_nicer_samples(
        eos_posterior, eos_prior_set,
        nicer_data, mass_prior_kwargs_set, nicer_tag, outdir):
    for i, eos in enumerate(tqdm(eos_posterior.samples[eos_posterior.eos_column])):
        macro_data = pd.read_csv(eos_prior_set.get_macro_path(int(eos)))
        Mmax_loc = eos_posterior.samples.columns.get_loc("Mmax")
        eos_posterior.samples.iloc[i, Mmax_loc] = np.max(macro_data["M"])
        mass_prior_kwargs = mass_prior_kwargs_set[nicer_tag]
        if "m_max" not in mass_prior_kwargs.keys() and eos_posterior.samples.iloc[i, Mmax_loc] < 1.0  :
            # print(
            #     "warning Mmax < Mmin",
            #     "Mmax is",
            #     eos_posterior.samples.iloc[i, Mmax_loc],
            # )
            # EoS produces no samples in range of likelihood anyway
            eos_posterior.samples.iloc[i, Mmax_loc] = 1.0
            continue
    print(mass_prior_kwargs)
    mr_samples = weigh_by_density_estimate.generate_mr_samples(
        eos_posterior, eos_prior_set, FlatMassPrior, num_samples_per_eos=100,
        mass_prior_kwargs=mass_prior_kwargs
    )

    sample_weights = np.concatenate(
        [
            weigh_by_density_estimate.weigh_mr_samples(
                mr_samples_set[["M", "R"]], nicer_data
            )
            for mr_samples_set in [*np.array_split(mr_samples, 10)]
        ]
    )

    mr_samples[f"logweight_{nicer_tag}"] = sample_weights
    mr_samples.to_csv(
        f"{outdir}/{eos_posterior.label}_{nicer_tag}_post.csv", index=False
    )
    eos_post = marginalize_over_mr_samples(mr_samples, nicer_tag=nicer_tag)
    #eos_post["eos"] = eos_posterior.samples["eos"]
    eos_post.to_csv(f"{outdir}/{eos_posterior.label}_{nicer_tag}_eos.csv", index=False)



if __name__ == "__main__":
    main_dir = ".."
    eos_base_directory = "/home/isaac.legred/RMFGP/gp-rmf-inference/conditioned-priors/11233/"
    outdir = "."
    nicer_mr_sets = {
        "Miller_J0740": pd.read_csv("./Miller_J0740.csv")}
        "Miller_J0030": pd.read_csv("./Miller_J0030_three-spot.csv"),
        "Choudhury_J0437": pd.read_csv("./Choudhury_J0437_headline.csv")}
    mass_prior_kwargs_set = {
        "Miller_J0740" : {"m_min": 1.0},
        "Miller_J0030" : {"m_min": 1.0, "m_max":1.8},
        "Choudhury_J0437" : {"m_min": 1.2, "m_max":1.6}
        
    }
    for eos_set in [
            "11233_maxpc2-1e11_mrgagn_01d000_00d010",
            "11233_maxpc2-1e12_mrgagn_01d000_00d010",
            "11233_maxpc2-1e13_mrgagn_01d000_00d010",
            "11233_maxpc2-1e14_mrgagn_01d000_00d010"
    ]:
        # List of indices of EOSs I use
        eos_posterior = EoSPosterior.from_csv(f"{main_dir}/{eos_set}.csv", label=eos_set)
        eos_dir = f"{eos_base_directory}/{eos_set}"
        eos_per_dir = 1000
        eos_tag = eos_set
        eos_posterior = result.EoSPosterior.from_csv(
            f"{main_dir}/{eos_tag}.csv", label=eos_tag
        )
        eos_prior_set = eos_prior.EoSPriorSet(
            eos_dir=eos_dir,
            eos_per_dir=eos_per_dir,
            macro_dir=eos_dir,
            macro_path_template="macro-draw-%(draw)06d.csv",
            eos_column="eos",
        )

        for nicer_tag in nicer_mr_sets:
            nicer_data = nicer_mr_sets[nicer_tag]
            weigh_eoss_by_nicer_samples(
                eos_posterior, eos_prior_set,
                nicer_data, mass_prior_kwargs_set, nicer_tag, outdir)

