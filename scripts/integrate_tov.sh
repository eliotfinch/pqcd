#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate /home/eliot.finch/eos/env/

# Function to run the Python script with the required arguments
run_bash_script() {
    eos="$1"
    eos_dir="$2"
    outpath_suffix="macro-"

    # Construct the command
    command=(
        "python"
        "/home/eliot.finch/eos/universality/bin/integrate-tov"
        "$eos_dir/$eos"
        "1e10"
        "1e16"
        "--outpath" "$eos_dir/$outpath_suffix$eos"
        "--central-eos-column" "baryon_density"
        "--formalism" "logenthalpy_MRLambda"
    )

    # Run the command
    "${command[@]}"
}

set_number=11
N_samples=50000

for variety in 'had' 'hyp' 'qrk'; do
    variety_dir="/home/eliot.finch/eos/pqcd/data/eos-draws-modified/$(printf '%02d' $set_number)/${variety}agn"
    for eos_dir in "$variety_dir"/*/; do
        if [ -d "$eos_dir" ]; then
            for eos_path in "$eos_dir"/*; do
                eos=$(basename "$eos_path")
                run_bash_script "$eos" "$eos_dir"
            done
        fi
    done
done
