import subprocess

def run_bash_script(eos, eos_dir=".", numerical_args=("1e10", "1e16"), outpath_suffix="macro-"):
    
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

sets = [11]
N_samples = 50000

for s in sets:
    for variety in ['had', 'hyp']:
        for n in range(N_samples):
            try:
                eos_dir = f'/home/eliot.finch/eos/pqcd/data/eos-draws-modified/{s:02}/{variety}agn/DRAWmod1000-{int(n/1000):06}'
                run_bash_script(f'eos-draw-{n:06}.csv', eos_dir=eos_dir)
            except:
                pass