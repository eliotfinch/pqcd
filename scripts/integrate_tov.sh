#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate /home/eliot.finch/eos/env/

run_bash_script() {
    eos=$1
    eos_dir=$2
    numerical_args=("1e10" "1e16")
    outpath_suffix="macro-"

    command=(
        "python"
        "/home/eliot.finch/eos/universality/bin/integrate-tov"
        "${eos_dir}/${eos}"
        "${numerical_args[0]}"
        "${numerical_args[1]}"
        "--outpath" "${eos_dir}/${outpath_suffix}${eos}"
        "--central-eos-column" "baryon_density"
        "--formalism" "logenthalpy_MRLambda"
    )

    "${command[@]}"
}

sets=(0 1 2 3 4)
N_samples=1000

for s in "${sets[@]}"; do
    for variety in "had" "hyp" "qrk"; do
        eos_dir="/home/eliot.finch/eos/pqcd/data/eos-draws-modified/$(printf "%02d" "$s")/${variety}agn"
        for ((i=0; i<N_samples; i++)); do
            run_bash_script "$(printf "eos-draw-%06d.csv" "$i")" "$eos_dir"
        done
    done
done

