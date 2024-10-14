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

set_number=12

# Loop over each variety type ('had', 'hyp', 'qrk')
for variety in 'had' 'hyp' 'qrk'; do
    # Define the directory path for the current variety
    # Using $(printf '%02d' $set_number) to format set_number as two digits (e.g., '01', '02')
    variety_dir="/home/eliot.finch/eos/pqcd/data/eos-draws-modified/$(printf '%02d' $set_number)/${variety}agn"

    # Loop over each subdirectory in the current variety directory
    for eos_dir in "$variety_dir"/*/; do
        # Check if the current path is a directory
        if [ -d "$eos_dir" ]; then
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
        fi
    done
done
