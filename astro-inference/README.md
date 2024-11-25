# Applying astro constraints

_On cluster_:
1. Create `margagn` via `scripts/create_margagn.py`.
2. Run `astro-inference/get_eos_files.py`
3. Run `astro-inference/RADIO/weight_eos_set_by_pulsar.py`
4. Run `astro-inference/XRAY/analyze_nicer.py`
5. Run `astro-inference/GW/generate_config.py`
6. Run `lwp-pipe gw_170817.ini`, `lwp-pipe gw_190425.ini`

_Locally_:

Copy weights to (for example) `data/eos-draws-modified/12/astro-weights` and run `combine_weights.ipynb`. We can then run `scripts/temperance_modified_quantiles.py`, but note that mass-radius and mass-lambda quantiles are not working because I need to calculate the moment of inertia.