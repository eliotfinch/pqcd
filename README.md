# pqcd

Investigations into incorporating constraints from perturbative quantum chromodynamics (pQCD) into neutron-star equation-of-state (EOS) inference.

## The `pqcd` package

The `pqcd.pQCD` class is initialised with a value for the dimensionless renormalization scale X, and gives you the predicted pQCD energy density, pressure, and baryon number density as a function of the baryon chemical potential. The code is taken from the [data release](https://zenodo.org/records/7781233) associated with [Gorda et al. 2023](https://arxiv.org/abs/2204.11877).

The "maximized" pQCD likelihood (from the same data release) is found in `pqcd.likelihood`. This likelihood has minimal assumptions about the EOS behavior above the density at which the likelihood is applied.

In [Komoltsev et al. 2024](https://arxiv.org/abs/2312.14127), an alternative likelihood which explicitly models the EOS up to pQCD densities is proposed (available in this [data release](https://zenodo.org/records/10592568)). In the paper we refer to this as the "modeled" likelihood, but in the code it is referred to as the "marginalised" likelihood for historic reasons (see `pqcd.likelihood`).

The file `pqcd.constraints` contains a re-implementation of the functions described in [Komoltsev & Kurkela 2022](http://arxiv.org/abs/2111.05350), with some additional functions for visualization of the constraints.

## Data

Much of the code in this repository relies on data currently only available on the LIGO-Caltech computing cluster at

`ldas-grid:/home/eliot.finch/eos/pqcd/data`

The file `data/eos-draws-default/collated_np_all_post.csv` is a copy of the file found at

`ldas-grid:/home/isaac.legred/PTAnalysis/Analysis`,

and is a summary of the EOS draws found at

`ldas-grid:/home/philippe.landry/nseos/eos/gp/mrgagn`.

## Figures in *Finch et al. 2025*

Below I detail the relevant code to generate figures in *Finch et al. 2025*.

### Fig. 1

See [`notebooks/pqcd_calculations.ipynb`](notebooks/pqcd_calculations.ipynb). All dependencies are included in the repository.

### Fig. 2

See [`notebooks/maximised_likelihood_explanation.ipynb`](notebooks/maximised_likelihood_explanation.ipynb). The example EOS in the figure is not provided in the repository.

### Fig. 3

See [`notebooks/max_vs_marg.ipynb`](notebooks/max_vs_marg.ipynb). This makes use of the "EOS extensions" provided in [this data release](https://zenodo.org/records/10592568).

### Figs. 4 and 5

See [`notebooks/plot_pressure_vs_energy_density.ipynb`](notebooks/plot_pressure_vs_energy_density.ipynb). This depends on

 - The "EOS extensions" provided in [this data release](https://zenodo.org/records/10592568).
 - Values of the "default" EOS draws (referred to as the "low-density" EOS in the paper) at 10nsat, obtained via [`scripts/get_epsilon_p_at_n.py`](scripts/get_epsilon_p_at_n.py).
 - Quantiles, calculated via [`scripts/quantiles/prior_quantiles.py`](scripts/quantiles/prior_quantiles.py), [`pqcd_quantiles.py`](scripts/quantiles/pqcd_quantiles.py), and [`pqcd_quantiles_marg.py`](scripts/quantiles/pqcd_quantiles_marg.py). These scripts in-turn depend on pQCD weights calculated via scripts in [`scripts/pqcd-weights`](scripts/pqcd-weights). A modified version of the `collated_np_all_post.csv` file which includes these weights is created in [`notebooks/edit_collated_eos.ipynb`](notebooks/edit_collated_eos.ipynb).

### Fig. 6

See [`notebooks/gp_summary_plots.ipynb`](notebooks/gp_summary_plots.ipynb). This depends on

 - Values of the "default" EOS draws (referred to as the "low-density" EOS in the paper) at nTOV, obtained via [`scripts/get_epsilon_p_at_n.py`](scripts/get_epsilon_p_at_n.py).
 - Quantiles, calculated via [`scripts/quantiles/prior_quantiles.py`](scripts/quantiles/prior_quantiles.py) and [`astro_quantiles.py`](scripts/quantiles/astro_quantiles.py). Note that we re-generate the astro weights for the low-density "default" EOS via scripts in [`astro-inference`](astro-inference), and as in Figs. 4 and 5 this also requires the pQCD weights calculated via scripts in [`scripts/pqcd-weights`](scripts/pqcd-weights).

### Fig. 7

See [`notebooks/plot_p_epsilon_at_ntov.ipynb`](notebooks/plot_p_epsilon_at_ntov.ipynb). This depends on values of the "default" EOS draws at nTOV and the pQCD weights, as above.

### Fig. 8

See [`notebooks/plot_pqcd_window.ipynb`](notebooks/plot_pqcd_window.ipynb). All dependencies are included in the repository.

### Fig. 9

See [`notebooks/gp_summary_plots.ipynb`](notebooks/gp_summary_plots.ipynb). This depends on the "GP2" EOS draws (referred to as the "unified" GP in the paper). These are generated with the following process:

 - The GP is created via [`notebooks/custom_gp.ipynb`](notebooks/custom_gp.ipynb) (see also the README inside [`scripts/eos-draw`](scripts/eos-draw)).
 - Draws from the GP are generated via scripts in [`scripts/eos-draw/gp2-parallel`](scripts/eos-draw/gp2-parallel) (note that currently these scripts only exist on the LIGO-Caltech computing cluster).
 - The draws that are consistent with pQCD are filtered out using [`scripts/eos-filter/filter_eos_draws_gp2_parallel.py`](scripts/eos-filter/filter_eos_draws_gp2_parallel.py). The pQCD-consistent draws are copied to `data/eos-draws-modified/gp2/margagn`.
 - Neutron-star mass-radius curves and tidal deformabilities are obtained via [`scripts/eos-integrate/integrate_tov_gp2_parallel.sh`](scripts/eos-integrate/integrate_tov_gp2_parallel.sh).

Then, as for Fig. 6, astrophysical weights are calculated via scripts in [`astro-inference`](astro-inference), and quantiles are calculated via [`scripts/quantiles/prior_quantiles_modified.py`](scripts/quantiles/prior_quantiles_modified.py) and [`astro_quantiles_modified.py`](scripts/quantiles/astro_quantiles_modified.py).

### Fig. 10

See [`notebooks/plot_modified_quantities_at_ntov.ipynb`](notebooks/plot_modified_quantities_at_ntov.ipynb). This depends on the values of "GP2" at nTOV, which are obtained via [`scripts/get_modified_gp_tov_quantities.py`](scripts/get_modified_gp_tov_quantities.py).

### Fig. 11

See [`notebooks/tov_corner.ipynb`](notebooks/tov_corner.ipynb). As for Figs. 7 and 10, this depends on the values of the "default" GP and "GP2" at nTOV.

### Fig. 12

See [`notebooks/max_vs_marg.ipynb`](notebooks/max_vs_marg.ipynb). All dependencies are included in the repository.

### Fig. 13

See [`notebooks/maximised_likelihood_explanation.ipynb`](notebooks/maximised_likelihood_explanation.ipynb). All dependencies are included in the repository.

### Fig. 14

See [`notebooks/generate_random_walk_eos.ipynb`](notebooks/generate_random_walk_eos.ipynb). All dependencies are included in the repository.

### Fig. 15

See [`notebooks/plot_unfied_mu_n.ipynb`](notebooks/plot_unfied_mu_n.ipynb). This depends on EOS draws from "GP2".

### Fig. 16

See [`notebooks/gp_summary_plots.ipynb`](notebooks/gp_summary_plots.ipynb). This depends on the "GP1" EOS draws (referred to as the "intermediate" GP in the paper). These are generated following the same process as for "GP2" (see Fig. 9).
