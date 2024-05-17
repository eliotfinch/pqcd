#!/home/eliot.finch/eos/env/bin/python

import subprocess

def run_bash_script(eos, eos_dir=".", numerical_args=("1e10", "1e16"), outpath_suffix="macro-"):
    # Construct the command
    command = [
        "python", 
        "/Users/eliot/Documents/Research/EOS/universality/bin/integrate-tov",
        f"{eos_dir}/{eos}",
        '1e10',
        '1e16',
        "--outpath", f"{eos_dir}/{outpath_suffix}{eos}",
        "--central-eos-column", "baryon_density",
        "--formalism", "logenthalpy_MRLambda"
    ]
    
    # Run the command
    subprocess.run(command)

sets = [1,2,3,4]
N_samples = 1000

for s in sets:
    for variety in ['had', 'hyp', 'qrk']:
        eos_dir = f'/Users/eliot/Documents/Research/EOS/pqcd/data/eos-draws-modified/{s:02}/{variety}agn'
        for i in range(N_samples):
            run_bash_script(f'eos-draw-{i:06}.csv', eos_dir=eos_dir)