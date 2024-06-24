import subprocess
from pathlib import Path

def run_bash_script(eos, eos_dir=".", outpath_suffix="macro-"):
    
    # Construct the command
    command = [
        "python", 
        "/home/eliot.finch/eos/universality/bin/integrate-tov",
        f"{eos_dir}/{eos}",
        '1e10',
        '1e16',
        "--outpath", f"{eos_dir}/{outpath_suffix}{eos}",
        "--central-eos-column", "baryon_density",
        "--formalism", "logenthalpy_MRLambda"
    ]
    
    # Run the command
    subprocess.run(command)

set_number = 11
N_samples = 50000

for variety in ['had', 'hyp', 'qrk']:
    variety_dir = Path(f'/home/eliot.finch/eos/pqcd/data/eos-draws-modified/{set_number:02}/{variety}agn')
    for eos_dir in [f for f in variety_dir.iterdir() if f.is_dir()]:
        for eos_path in eos_dir.iterdir():
            run_bash_script(eos_path.name, eos_dir=eos_dir)