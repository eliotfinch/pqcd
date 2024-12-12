import pandas as pd

import configparser
import os

config = configparser.ConfigParser()


def generate_config(
        eos_directory,
        eos_per_dir,
        eos_tag,
        eos_indices_file,
        gw_posterior_samples,
        gw_posterior_in_file,
        outtag
):

    in_data = pd.read_csv(gw_posterior_in_file, index_col=0)
    cwd = os.getcwd()

    def local(path, cwd):
        return os.path.join(cwd, path)

    config["Samples"] = {
        "eos-directory": eos_directory,
        "eos-per-dir": eos_per_dir,
        "eos-indices": eos_indices_file,
        "gw-posterior-samples": local(gw_posterior_samples, cwd),
        "bandwidth-file": local(gw_posterior_in_file, cwd)
    }

    config["Marginalization"] = {
        "prior": "default",
        "chirp-mass-range": str((
            0.99 * in_data.loc["mc", "lb"],
            1.01 * in_data.loc["mc", "ub"]
        )),
        "mass-ratio-range": str((
            0.99 * in_data.loc["q", "lb"],
            min(1.01 * in_data.loc["q", "ub"], 1.0)
        ))
    }

    config["Submission"] = {
        "label": f"{outtag}",
        "format-for-condor": "True",
        "condor-num-jobs": "10",
        "accounting": "ligo.sim.o4.cbc.extremematter.bilby",
        "submit-dag": "True",
        "merge-executable": "/home/isaac.legred/lwp/bin/combine-samples",
        "condor-kwargs": {
            "request_disk": "10 MB",
            "request_memory": "2048 MB",
            "universe": "vanilla"
        }
    }

    config["Output"] = {
        "save-marginalized-likelihoods": f"{outtag}_eos.csv",
        "save-likelihoods": f"{outtag}_post.csv",
        "macro-prefix": "macro-draw",
        "output-dir": os.path.join(cwd, eos_tag, outtag)
    }

    with open(f"{eos_tag}/{outtag}.ini", "w") as configfile:
        config.write(configfile)


def generate_170817_and_190425_inis(
        eos_tag,
        eos_directory,
        eos_indices_file,
        eos_per_dir=1000
):

    cwd = os.getcwd()

    outtag_170817 = "gw_170817"

    gw_posterior_samples_170817 = f"{cwd}/LVC_GW170817_PhenomPNRT-lo.csv"
    gw_posterior_in_file_170817 = f"{cwd}/LVC_GW170817_PhenomPNRT-lo.in"

    generate_config(
        eos_directory,
        eos_per_dir,
        eos_tag,
        eos_indices_file,
        gw_posterior_samples_170817,
        gw_posterior_in_file_170817,
        outtag_170817
    )

    outtag_190425 = "gw_190425"

    gw_posterior_samples_190425 = f"{cwd}/PE190425_low_spin_bilby.csv"
    gw_posterior_in_file_190425 = f"{cwd}/PE190425_low_spin_bilby.in"

    generate_config(
        eos_directory,
        eos_per_dir,
        eos_tag,
        eos_indices_file,
        gw_posterior_samples_190425,
        gw_posterior_in_file_190425,
        outtag_190425
    )


if __name__ == "__main__":

    eos_tag = "margagn"
    eos_per_dir = 1000
    eos_directory = "/home/philippe.landry/nseos/eos/gp/mrgagn"
    eos_indices_file = (
        "/home/eliot.finch/eos/pqcd/data/eos-draws-default/"
        "margagn-manifest.csv"
    )

    if not os.path.exists(eos_tag):
        os.mkdir(eos_tag)

    generate_170817_and_190425_inis(
        eos_tag,
        eos_directory,
        eos_indices_file,
        eos_per_dir
    )
