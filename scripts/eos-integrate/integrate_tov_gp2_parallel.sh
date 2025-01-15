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

target_dir="/home/eliot.finch/eos/pqcd/data/eos-draws-modified/gp2/margagn"

# Specify which DRAWmod1000 dirs to integrate (to avoid re-integrating everything)
folders=(DRAWmod1000-0000{20..37})
for folder in "${folders[@]}"; do
    eos_dir="$target_dir/$folder"
    # Loop over each file in the current eos_dir directory that begins with "eos-draw"
    for eos_path in "$eos_dir"/eos-draw*; do
        # Check if the current path is a file
        if [ -f "$eos_path" ]; then
            # Extract the filename (basename) from the path
            eos=$(basename "$eos_path")
            
            # Call a function or script with the current filename and directory as arguments
            run_bash_script "$eos" "$eos_dir"
        fi
    done
done
