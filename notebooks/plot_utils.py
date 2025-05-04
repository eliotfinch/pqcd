import numpy as np

from matplotlib.colors import to_hex, to_rgba
from cmcrameri import cm
from pqcd.utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre,
    )

rcparams = {
    'font.size': 14,
    'axes.titlesize': 14,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'font.family': 'serif',
    'font.sans-serif': ['Computer Modern Roman'],
    'text.usetex': True,
    }

# Values that the quantiles are built on

x_pe = to_GeV_per_cubic_femtometre(np.linspace(5e13, 3e16, 1000))
x_cn = to_nucleons_per_cubic_femtometre(np.linspace(2.8e13, 1.5e16, 1000))
y_mr = np.linspace(0.5, 2.5, 1000)

# Axis limits

xlim_pe = (0.13471795348380078, 17.002209254489188)
ylim_pe = (0.0014798402249155988, 6.262273589369166)

xlim_cn = (x_cn[0], 7.20534255445628)
ylim_cn = (0, 1)

xlim_mr = (6, 18)
ylim_mr = (y_mr[0], y_mr[-1])

xlim_mtov = (1.5, 3.5)

# Colors and linestyles

prior_c = '#cccccc'
astro_c = to_hex(cm.roma(0.9))

gp0_pqcd_c = to_hex('dimgray')
gp0_pqcd_ls = '--'

gp0_astro_pqcd_max_c = to_hex('C1')
gp0_astro_pqcd_max_ls = '--'

gp0_astro_pqcd_mod_c = to_hex('C3')
gp0_astro_pqcd_mod_ls = ':'

# kwargs

prior_kwargs = dict(
    lw=0,
    zorder=0.1,
    color=prior_c,
)

astro_hist_kwargs = dict(
    histtype='stepfilled',
    edgecolor=astro_c,
    lw=2,
    color=list(to_rgba(astro_c))[:3] + [0.1]
)

astro_fill_kwargs = dict(
    lw=0,
    zorder=0.9,
    facecolor=list(to_rgba(astro_c))[:3] + [0.1]
)

astro_line_kwargs = dict(
    lw=2,
    zorder=1,
    c=astro_c
)

gp0_pqcd_kwargs = dict(
    lw=2,
    ls=gp0_pqcd_ls,
    zorder=1.1,
    c=gp0_pqcd_c
)

gp0_astro_pqcd_max_hist_kwargs = dict(
    histtype='step',
    color=to_rgba(gp0_astro_pqcd_max_c),
    lw=2,
    linestyle=gp0_astro_pqcd_max_ls,
)

gp0_astro_pqcd_max_kwargs = dict(
    lw=2,
    ls=gp0_astro_pqcd_max_ls,
    zorder=1.1,
    c=gp0_astro_pqcd_max_c
)

gp0_astro_pqcd_mod_hist_kwargs = dict(
    histtype='step',
    color=to_rgba(gp0_astro_pqcd_mod_c),
    lw=2,
    linestyle=gp0_astro_pqcd_mod_ls,
)

gp0_astro_pqcd_mod_kwargs = dict(
    lw=2,
    ls=gp0_astro_pqcd_mod_ls,
    zorder=1.1,
    c=gp0_astro_pqcd_mod_c
)
