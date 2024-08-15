import subprocess
from pathlib import Path

def run_bash_script(eos_number, eos_dir):
    
    # Construct the command
    command = [
        "python", 
        "/home/eliot.finch/eos/universality/bin/integrate-tov",
        f"{eos_dir}/eos-draw-{eos_number:06}.csv",
        '1e10',
        '1e16',
        "--outpath", f"{eos_dir}/macro-draw-{eos_number:06}.csv",
        "--central-eos-column", "baryon_density",
        "--formalism", "logenthalpy_MRLambda"
    ]
    
    # Run the command 
    subprocess.run(command)

set_number = 12
varieties = ['had', 'hyp', 'qrk']

set_dir = Path(f'/home/eliot.finch/eos/pqcd/data/eos-draws-modified/{set_number:02}')

for variety in varieties:

    var_dir = set_dir / f'{variety}agn'

    # Get the list of DRAWmod1000 directories
    drawmod_dirs = [
        f.name for f in var_dir.iterdir() 
        if f.is_dir() and f.name.startswith('DRAWmod1000')
        ]

    for drawmod_dir in drawmod_dirs:

        drawmod_var_dir = var_dir / drawmod_dir

        # Get the list of eos-draw numbers
        eos_draw_files = [
            f.name for f in drawmod_var_dir.iterdir() 
            if f.is_file() and f.name.startswith('eos')
            ]
        
        eos_numbers = [
            int(f.split('-')[-1].split('.')[0]) for f in eos_draw_files
        ]

        # Get the list of macro-draw numbers
        macro_draw_files = [
            f.name for f in drawmod_var_dir.iterdir() 
            if f.is_file() and f.name.startswith('macro')
            ]
        
        macro_numbers = [
            int(f.split('-')[-1].split('.')[0]) for f in macro_draw_files
        ]

        for eos_number in eos_numbers:
            if eos_number not in macro_numbers:
                run_bash_script(eos_number, eos_dir=drawmod_var_dir)