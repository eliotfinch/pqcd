#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate /home/eliot.finch/eos/env/

# Function to run the bash script
run_bash_script() {
    eos_number=$1
    eos_dir=$2
    
    # Construct and run the command
    python /home/eliot.finch/eos/universality/bin/integrate-tov \
        "${eos_dir}/eos-draw-$(printf "%06d" $eos_number).csv" \
        "1e10" "1e16" \
        --outpath "${eos_dir}/macro-draw-$(printf "%06d" $eos_number).csv" \
        --central-eos-column "baryon_density" \
        --formalism "logenthalpy_MRLambda"
}

# Set variables
set_number=12
varieties=("had" "hyp" "qrk")
set_dir="/home/eliot.finch/eos/pqcd/data/eos-draws-modified/$(printf "%02d" $set_number)"

for variety in "${varieties[@]}"; do

    var_dir="${set_dir}/${variety}agn"

    # Get the list of DRAWmod1000 directories
    drawmod_dirs=()
    while IFS=  read -r -d $'\0'; do
        drawmod_dirs+=("$REPLY")
    done < <(find "$var_dir" -maxdepth 1 -type d -name "DRAWmod1000*" -print0)

    for drawmod_dir in "${drawmod_dirs[@]}"; do

        drawmod_var_dir="${drawmod_dir}"

        # Get the list of eos-draw numbers
        eos_draw_files=()
        while IFS=  read -r -d $'\0'; do
            eos_draw_files+=("$REPLY")
        done < <(find "$drawmod_var_dir" -maxdepth 1 -type f -name "eos-*.csv" -print0)

        eos_numbers=()
        for f in "${eos_draw_files[@]}"; do
            eos_numbers+=($(basename "$f" | awk -F'-' '{print $NF}' | sed 's/\.csv//'))
        done

        # Get the list of macro-draw numbers
        macro_draw_files=()
        while IFS=  read -r -d $'\0'; do
            macro_draw_files+=("$REPLY")
        done < <(find "$drawmod_var_dir" -maxdepth 1 -type f -name "macro-*.csv" -print0)

        macro_numbers=()
        for f in "${macro_draw_files[@]}"; do
            macro_numbers+=($(basename "$f" | awk -F'-' '{print $NF}' | sed 's/\.csv//'))
        done

        for eos_number in "${eos_numbers[@]}"; do
            if [[ ! " ${macro_numbers[@]} " =~ " ${eos_number} " ]]; then
                run_bash_script "$eos_number" "$drawmod_var_dir"
            fi
        done
    done
done
