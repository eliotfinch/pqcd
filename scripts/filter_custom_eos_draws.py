#!/home/eliot.finch/eos/env/bin/python

import pandas as pd

import shutil
import os
import pqcd

source_dir = '/home/eliot.finch/eos/pqcd/make-agnostic-processes-tests'
destination_dir = '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/17'

labels = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
]

success_counts = {label: 0 for label in labels}

N_samp = 2000

pqcd_region_dict = pqcd.get_pqcd_region(mu_high=3, res=200)

for label in labels:
    success_count = success_counts[label]
    for n in range(N_samp):
        source_path = f'{source_dir}/cus{label}agn/DRAWmod1000-{int(n/1000):06}'
        eos = pd.read_csv(f'{source_path}/eos-draw-{n:06}.csv')
        if pqcd.consistent_with_pqcd(eos, pqcd_region_dict):
            destination_path = f'{destination_dir}/cus{label}agn/DRAWmod1000-{int(success_count/1000):06}'
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            shutil.copy(f'{source_path}/eos-draw-{n:06}.csv', f'{destination_path}/eos-draw-{success_count:06}.csv')
            shutil.copy(f'{source_path}/draw-gpr_cus{label}agn-{n:06}.csv', f'{destination_path}/draw-gpr_cus{label}agn-{success_count:06}.csv')
            success_count += 1
