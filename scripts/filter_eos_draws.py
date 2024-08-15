#!/home/eliot.finch/eos/env/bin/python

import pandas as pd

import shutil
import os
import pqcd

from pathlib import Path

source_dir = Path('/home/eliot.finch/eos/pqcd/make-agnostic-processes')
destination_dir = Path('/home/eliot.finch/eos/pqcd/data/eos-draws-modified/12')

varieties = ['had', 'hyp', 'qrk']
success_counts = {}

for variety in varieties:

    var_dest_dir = destination_dir / f'{variety}agn'

    # Get the list of DRAWmod1000 directories
    drawmod_dirs = [
        f.name for f in var_dest_dir.iterdir() 
        if f.is_dir() and f.name.startswith('DRAWmod1000')
        ]

    # We care about the largest DRAWmod1000 directory
    drawmod_dir = sorted(drawmod_dirs)[-1]

    drawmod_dest_dir = var_dest_dir / drawmod_dir

    # Get the list of eos-draw files
    eos_draw_files = [
        f.name for f in drawmod_dest_dir.iterdir() 
        if f.is_file() and f.name.startswith('eos-draw')
        ]
    
    eos_numbers = []
    for f in eos_draw_files:
        eos_numbers.append(int(f.split('-')[-1].split('.')[0]))

    success_counts[variety] = max(eos_numbers) + 1

print(success_counts)

# N_samp = 50000

# pqcd_region_dict = pqcd.get_pqcd_region(mu_high=3, res=200)

# for variety in varieties:
#     success_count = success_counts[variety]
#     for n in range(N_samp):
#         source_path = source_dir / f'{variety}agn/DRAWmod1000-{int(n/1000):06}'
#         eos = pd.read_csv(source_path / f'eos-draw-{n:06}.csv')
#         if pqcd.consistent_with_pqcd(eos, pqcd_region_dict):
#             destination_path = destination_dir / f'{variety}agn/DRAWmod1000-{int(success_count/1000):06}'
#             if not os.path.exists(destination_path):
#                 os.makedirs(destination_path)
#             shutil.copy(source_path / f'eos-draw-{n:06}.csv', destination_path / f'eos-draw-{success_count:06}.csv')
#             shutil.copy(source_path / f'draw-gpr_{variety}agn-{n:06}.csv', destination_path / f'draw-gpr_{variety}agn-{success_count:06}.csv')
#             success_count += 1
