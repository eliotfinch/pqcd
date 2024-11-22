import shutil
from pathlib import Path

eos_dir = Path('../data/eos-draws-modified/24')

# labels = ['had', 'hyp', 'qrk']
labels = [
    'cusa', 
    'cusb',
    'cusc',
    'cusd',
    'cuse',
    'cusf',
    'cusg',
    'cush',
    'cusi',
    'cusj'
]

print('Counting number of eos draws...')

eos_counts = {}

for label in labels:

    label_dest_dir = eos_dir / f'{label}agn'

    # Get the list of DRAWmod1000 directories
    drawmod_dirs = [
        f.name for f in label_dest_dir.iterdir()
        if f.is_dir() and f.name.startswith('DRAWmod1000')
        ]

    # We care about the largest DRAWmod1000 directory
    drawmod_dir = sorted(drawmod_dirs)[-1]

    drawmod_dest_dir = label_dest_dir / drawmod_dir

    # Get the list of eos-draw files
    eos_draw_files = [
        f.name for f in drawmod_dest_dir.iterdir()
        if f.is_file() and f.name.startswith('eos-draw')
        ]

    eos_numbers = []
    for f in eos_draw_files:
        eos_numbers.append(int(f.split('-')[-1].split('.')[0]))

    eos_counts[label] = max(eos_numbers) + 1

print(eos_counts)

marg_count = 0
for variety, count in eos_counts.items():
    for n in range(count):

        source_dir = eos_dir / f'{variety}agn/DRAWmod1000-{int(n/1000):06}'
        destination_dir = \
            eos_dir / f'margagn/DRAWmod1000-{int((marg_count+n)/1000):06}'

        source_gp = source_dir / f'draw-gpr_{variety}agn-{n:06}.csv'
        destination_gp = \
            destination_dir / f'draw-gpr_margagn-{marg_count+n:06}.csv'

        source_eos = source_dir / f'eos-draw-{n:06}.csv'
        destination_eos = destination_dir / f'eos-draw-{marg_count+n:06}.csv'

        source_macro = source_dir / f'macro-eos-draw-{n:06}.csv'
        destination_macro = \
            destination_dir / f'macro-eos-draw-{marg_count+n:06}.csv'

        # Copy files
        destination_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_gp, destination_gp)
        shutil.copy(source_eos, destination_eos)
        shutil.copy(source_macro, destination_macro)

    marg_count += count
