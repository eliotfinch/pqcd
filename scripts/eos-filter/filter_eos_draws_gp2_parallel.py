#!/home/eliot.finch/eos/env/bin/python

import pandas as pd

import shutil
import pqcd

from pathlib import Path

source_dir = Path('/home/eliot.finch/eos/pqcd/gp2-parallel')
destination_dir = Path(
    '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/25/margagn'
)
destination_dir.mkdir(parents=True, exist_ok=True)

# Number of parallel runs
n_runs = 10

# Number of EOS draws in each run
n_samp = 10000

# You can loop over a string to take each character in turn
labels = 'abcdefghijklmnopqrst'

# Count exisiting draws
# ---------------------

print('Counting number of exisiting eos draws...')

# Get the list of DRAWmod1000 directories
drawmod_dirs = [
    f.name for f in destination_dir.iterdir()
    if f.is_dir() and f.name.startswith('DRAWmod1000')
    ]

if len(drawmod_dirs) > 0:

    # We care about the largest DRAWmod1000 directory
    drawmod_dir = sorted(drawmod_dirs)[-1]

    drawmod_dest_dir = destination_dir / drawmod_dir

    # Get the list of eos-draw files
    eos_draw_files = [
        f.name for f in drawmod_dest_dir.iterdir()
        if f.is_file() and f.name.startswith('eos-draw')
    ]

    eos_numbers = []
    for f in eos_draw_files:
        eos_numbers.append(int(f.split('-')[-1].split('.')[0]))

    success_counts = max(eos_numbers) + 1

else:

    success_counts = 0

print(success_counts)

# Filter
# ------

pqcd_region_dict = pqcd.get_pqcd_region(mu_high=3, res=200)

print('Copying eos files consistent with pQCD region...')

for n_run in range(n_runs):
    print(f'Processing run {n_run}...')
    for label in labels:
        print(f'Processing label {label}...')
        for n in range(n_samp):
            source_path = (
                source_dir / f'{n_run}'
                f'/cus{label}agn/DRAWmod1000-{int(n/1000):06}'
            )
            eos = pd.read_csv(source_path / f'eos-draw-{n:06}.csv')
            if pqcd.consistent_with_pqcd(eos, pqcd_region_dict):
                destination_path = (
                    destination_dir /
                    f'DRAWmod1000-{int(success_counts/1000):06}'
                )
                destination_path.mkdir(parents=True, exist_ok=True)
                shutil.copy(
                    source_path / f'eos-draw-{n:06}.csv',
                    destination_path / f'eos-draw-{success_counts:06}.csv'
                )
                shutil.copy(
                    source_path / f'draw-gpr_cus{label}agn-{n:06}.csv',
                    destination_path /
                    f'draw-gpr_margagn-{success_counts:06}.csv'
                )
                success_counts += 1

print(f'Success count = {success_counts}')
