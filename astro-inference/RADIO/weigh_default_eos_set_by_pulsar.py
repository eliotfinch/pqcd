#!/home/eliot.finch/eos/env/bin/python

import numpy as np
import pandas as pd

import temperance.weighing.weigh_by_pulsar as weigh_by_pulsar
from temperance.core.result import EoSPosterior


def pulsar_sample_likelihood(mmax_eos, mass_samples):
    return np.array(
        [np.sum(mass_samples < mmax)/len(mass_samples) for mmax in mmax_eos]
        )


def weigh_by_pulsar_data(pulsar_mass_sample_sets, eos_posterior, **kwargs):
    for sample_set in pulsar_mass_sample_sets.keys():
        weigh_by_pulsar.weigh_EoSs_by_mass_measurement(
            eos_posterior,
            likelihood=lambda mmax: pulsar_sample_likelihood(
                mmax, pulsar_mass_sample_sets[sample_set]["m"]
                ),
            weight_tag=sample_set,
            **kwargs
            )


if __name__ == "__main__":

    collated_eos = pd.read_csv(
        '../data/eos-draws-default/collated_np_all_post.csv'
    )
    blank_manifest = collated_eos[['eos', 'Mmax']]
    blank_manifest = blank_manifest.set_index('eos')
    blank_manifest.to_csv('../data/eos-draws-default/margagn-manifest.csv')

    eos_base_directory = (
        "/home/eliot.finch/eos/pqcd/data/eos-draws-default"
    )

    pulsar_mass_sets = {
        "Fonseca_J0740": pd.read_csv(
            "/home/isaac.legred/New_NICER/NoNSAnalysis/CalcSamples/"
            "Fonseca_J0740.csv"
        ),
        "Antoniadis_J0348": pd.read_csv(
            "/home/isaac.legred/New_NICER/NoNSAnalysis/CalcSamples/"
            "Antoniadis_J0348.csv"
        )
    }

    eos_posterior = EoSPosterior.from_csv(
        f"{eos_base_directory}/margagn-manifest.csv",
        label="margagn"
    )
    weigh_by_pulsar_data(pulsar_mass_sets, eos_posterior)
    eos_posterior.samples.to_csv("margagn.csv", index=False)
