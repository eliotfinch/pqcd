# Applying astro constraints

_On cluster_:

1. Run `astro-inference/get_eos_files.py`
2. Run `astro-inference/RADIO/weight_eos_set_by_pulsar.py`
3. Run `astro-inference/XRAY/analyze_nicer.py`
4. Run `astro-inference/GW/generate_config.py`
5. Run `lwp-pipe gw_170817.ini`, `lwp-pipe gw_190425.ini`

_Locally_:

Copy weights to (for example) `data/eos-draws-modified/gp2/astro-weights` and run `combine_weights.ipynb`. We can then run `scripts/quantiles/astro_quantiles_modified.py`.
The relevant GW weights are `gw_170817_eos.csv` and `gw_190425_eos.csv`.
