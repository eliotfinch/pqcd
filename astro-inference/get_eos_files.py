#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd
import temperance.sampling.eos_prior as tmeos_prior

import tqdm


def get_mmax(macro_data):
    dM_drho = np.gradient(
        macro_data["M"],
        macro_data["central_baryon_density"]
        )
    stable = np.where(dM_drho > 0)[0]
    return np.max(macro_data["M"][stable])


def get_eos_file(
        eos_directory,
        properties={"Mmax": get_mmax},
        num_eoss=10,
        eos_per_dir=1000
        ):
    """
    For each eos, get all of the properties specified in the properties
    (currently only can get properties from the "macro" file)
    """
    eos_prior_set = tmeos_prior.EoSPriorSet(
        eos_dir=eos_directory,
        eos_column="eos",
        eos_per_dir=eos_per_dir,
        macro_dir=eos_directory,
        macro_path_template='macro-eos-draw-%(draw)06d.csv',
        branches_data=None
        )
    eos_file = pd.DataFrame({"eos": np.arange(num_eoss)})
    for prop_name in properties.keys():
        eos_file[prop_name] = np.zeros(num_eoss)
    for eos_index in tqdm.trange(num_eoss):
        macro_data = pd.read_csv(eos_prior_set.get_macro_path(eos_index))
        for prop_name in properties.keys():
            eos_file.loc[eos_index, prop_name] = \
                properties[prop_name](macro_data)
    return eos_file


if __name__ == "__main__":

    gp_number = 2
    # count_dict = {'marg': 33841+1}
    count_dict = {'marg': 37207+1}

    for variety, count in count_dict.items():
        eos_file = get_eos_file(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
            f'gp{gp_number}/{variety}agn',
            num_eoss=count
            )
        eos_file.to_csv(
            '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/'
            f'gp{gp_number}/{variety}agn-manifest.csv',
            index=False
            )
