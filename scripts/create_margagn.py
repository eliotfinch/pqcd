# %%
import os
import shutil
from pathlib import Path

# %%
eos_dir = Path('../data/eos-draws-modified/12')

# %%
eos_counts = {
    'had': 305,
    'hyp': 338,
    'qrk': 437
}

marg_count = 0
for variety, count in eos_counts.items():
    for n in range(count):

        source_dir = eos_dir / f'{variety}agn/DRAWmod1000-{int(n/1000):06}'
        destination_dir = eos_dir / f'margagn/DRAWmod1000-{int((marg_count+n)/1000):06}'

        source_gp = source_dir / f'draw-gpr_{variety}agn-{n:06}.csv'
        destination_gp = destination_dir / f'draw-gpr_margagn-{marg_count+n:06}.csv'

        source_eos = source_dir / f'eos-draw-{n:06}.csv'
        destination_eos = destination_dir / f'eos-draw-{marg_count+n:06}.csv'

        source_macro = source_dir / f'macro-eos-draw-{n:06}.csv'
        destination_macro = destination_dir / f'macro-eos-draw-{marg_count+n:06}.csv'

        # Copy files
        destination_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_gp, destination_gp)
        shutil.copy(source_eos, destination_eos)
        shutil.copy(source_macro, destination_macro)

    marg_count += count



