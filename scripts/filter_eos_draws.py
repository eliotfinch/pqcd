#!/home/eliot.finch/eos/env/bin/python

import pandas as pd

import shutil
import os
import pqcd

source_dir = '/home/eliot.finch/eos/pqcd/make-agnostic-processes'
destination_dir = '/home/eliot.finch/eos/pqcd/data/eos-draws-modified/11'

N_samp = 50000

pqcd_region_dict = pqcd.get_pqcd_region(mu_high=3, res=200)

for variety in ['had', 'hyp']:
    for n in range(N_samp):
        source_path = f'{source_dir}/{variety}agn/DRAWmod1000-{int(n/1000):06}'
        eos = pd.read_csv(f'{source_path}/eos-draw-{n:06}.csv')
        if pqcd.consistent_with_pqcd(eos, pqcd_region_dict):
            destination_path = f'{destination_dir}/{variety}agn/DRAWmod1000-{int(n/1000):06}'
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            shutil.copy(f'{source_path}/eos-draw-{n:06}.csv', f'{destination_path}/eos-draw-{n:06}.csv')