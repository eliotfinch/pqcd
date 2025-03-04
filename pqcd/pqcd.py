import numpy as np

from scipy.integrate import cumulative_trapezoid
from .utils import (
    to_GeV_per_cubic_femtometre,
    to_nucleons_per_cubic_femtometre
)


def epsilon_func(mu, n, p):
    return -p + mu*n


def pressure_integral(mu, n, pL):
    return np.concatenate(([pL], pL + cumulative_trapezoid(n, mu)))

# The following functions are taken from
# https://zenodo.org/records/7781233

# See also
# https://github.com/OKomoltsev/QCD-likelihood-function/tree/main


GeV3_to_fm3 = 1.0e3/1.9732705**3

# Some chatGPT references for the constants (I haven't checked these)

# pQCD Pressure Expansion Constants
# -----------------------------------
#
# Constant:    C_A
# Definition:  Casimir of the adjoint representation (for SU(N_c))
# QCD Value:   3  (for N_c = 3)
#
# Constant:    N_f
# Definition:  Number of quark flavors included in the calculation.
# QCD Value:   3 (for light quarks: up, down, strange)
#              (or higher if including heavier quarks)
#
# Constant:    d_A
# Definition:  Dimension of the adjoint representation, given by N_c^2 - 1.
# QCD Value:   8  (for N_c = 3, corresponding to the eight gluons)
#
# Constant:    C_F
# Definition:  Casimir of the fundamental representation, given by
#              (N_c^2 - 1) / (2 * N_c)
# QCD Value:   4/3  (for N_c = 3)
#
# Constant:    gamma_E
# Definition:  Euler-Mascheroni constant, commonly appearing in dimensional
#              regularization.
# QCD Value:   ~0.5772


def PNLO(a_s):
    # Eqs. 12 and 13 of https://arxiv.org/abs/2303.02175.
    # 1 - (2/pi).
    return 1. - 0.637*a_s


def PNNLO(a_s, X):
    # I think Eqs. 15 and 16 of https://arxiv.org/abs/2303.02175, but I haven't
    # checked
    return -a_s**2*(-1.831 + 0.304*np.log(a_s)) + \
        a_s**2*(-2.706 - 0.912*np.log(X))


def PN3LO(a_s):
    # Eq. 17 of https://arxiv.org/abs/2303.02175 (also haven't checked)
    return 0.484816*a_s**3


def alpha_s(mu, X):
    # Eq. 9 in http://arxiv.org/abs/0912.1856. Note that
    # ((1/3)**2)/(0.378**2) = 0.777632, where 0.378 is the value used for
    # Lambda_MS (see page 8 in http://arxiv.org/abs/0912.1856).
    numerator = 4*np.pi*(1. - (64.*np.log(np.log(0.777632*mu**2*X**2))) /
                         (81.*np.log(0.777632*mu**2*X**2)))
    denominator = (9.*np.log(0.777632*mu**2*X**2))
    return numerator/denominator


def das_dmu(mu, X):
    numerator = -2.20644 - 2.79253*np.log(0.777632*mu**2*X**2) + \
        4.41288*np.log(np.log(0.777632*mu**2*X**2))
    denominator = mu*(np.log(0.777632*mu**2*X**2))**3
    return numerator/denominator


def d2as_dmu2(mu, X):
    numerator1 = 22.0644 + 2.79253*(np.log(0.777632*mu**2*X**2))**2 - \
        26.4773*np.log(np.log(0.777632*mu**2*X**2))
    numerator2 = np.log(0.777632*mu**2*X**2)*(
         13.3765 - 4.41288*np.log(np.log(0.777632*mu**2*X**2))
    )
    denominator = mu**2*(np.log(0.777632*mu**2*X**2))**4
    return (numerator1+numerator2)/denominator


def dp_das(a_s, X):
    dPNLO = -0.637
    dPNNLO = a_s*(-2.054 - 0.608*np.log(a_s) - 1.824*np.log(X))
    dPN3LO = 1.45445*a_s**2
    return dPNLO + dPNNLO + dPN3LO


def d2p_das2(a_s, X):
    d2PNNLO = -2.662 - 0.608*np.log(a_s) - 1.824*np.log(X)
    d2PN3LO = 2.9089*a_s
    return d2PNNLO + d2PN3LO


def pFD(mu):
    return (mu)**4/(108*np.pi**2)


def dpFD(mu):
    return mu**3/(27*np.pi**2)


def d2pFD(mu):
    return mu**2/(9*np.pi**2)


class pQCD:

    def __init__(self, X):
        self.X = 2.*X

    def pH(self, mu):  # GeV/fm^3
        a_s = alpha_s(mu, self.X)
        return pFD(mu)*GeV3_to_fm3*(
            PNLO(a_s) + PNNLO(a_s, self.X) + PN3LO(a_s)
        )

    def nH(self, mu):  # 1/fm^3
        a_s = alpha_s(mu, self.X)
        p_as = (PNLO(a_s) + PNNLO(a_s, self.X) + PN3LO(a_s))
        return GeV3_to_fm3*(
            dp_das(a_s, self.X)*das_dmu(mu, self.X)*pFD(mu) + p_as*dpFD(mu)
        )

    def epsilonH(self, mu):  # GeV/fm^3
        return epsilon_func(mu, self.nH(mu), self.pH(mu))

    def cs2H(self, mu):
        a_s = alpha_s(mu, self.X)
        p_as = (PNLO(a_s) + PNNLO(a_s, self.X) + PN3LO(a_s))

        dn_dmu1 = pFD(mu)*(d2p_das2(a_s, self.X)*(das_dmu(mu, self.X))**2 +
                           dp_das(a_s, self.X)*d2as_dmu2(mu, self.X))
        dn_dmu2 = 2.*dp_das(a_s, self.X)*das_dmu(mu, self.X)*dpFD(mu) + \
            p_as * d2pFD(mu)

        return self.nH(mu)/(mu*GeV3_to_fm3*(dn_dmu1+dn_dmu2))

# =============================================================================

# Functions for testing if an EOS passes through the pQCD region


def get_pqcd_region(X_low=0.5, X_high=2, mu_low=2.4, mu_high=2.6, res=100):

    X_array = np.linspace(X_low, X_high, res)
    mu_array = np.linspace(mu_low, mu_high, res)

    p_boundary_arrays = []
    n_boundary_arrays = []
    mu_boundary_arrays = []

    # Get the fixed-mu arrays first
    for mu in [mu_low, mu_high]:
        p_boundary_arrays.append(np.zeros(res))
        n_boundary_arrays.append(np.zeros(res))
        mu_boundary_arrays.append(np.zeros(res))
        for i, X in enumerate(X_array):
            pQCDX = pQCD(X)
            p_boundary_arrays[-1][i] = pQCDX.pH(mu)
            n_boundary_arrays[-1][i] = pQCDX.nH(mu)
            mu_boundary_arrays[-1][i] = mu

    # Get the fixed-X arrays next
    for X in [X_low, X_high]:
        p_boundary_arrays.append(np.zeros(res))
        n_boundary_arrays.append(np.zeros(res))
        mu_boundary_arrays.append(np.zeros(res))
        for i, mu in enumerate(mu_array):
            pQCDX = pQCD(X)
            p_boundary_arrays[-1][i] = pQCDX.pH(mu)
            n_boundary_arrays[-1][i] = pQCDX.nH(mu)
            mu_boundary_arrays[-1][i] = mu

    left_n_boundary = np.hstack([n_boundary_arrays[0], n_boundary_arrays[3]])
    right_n_boundary = np.hstack([n_boundary_arrays[2], n_boundary_arrays[1]])

    left_p_boundary = np.hstack([p_boundary_arrays[0], p_boundary_arrays[3]])
    right_p_boundary = np.hstack([p_boundary_arrays[2], p_boundary_arrays[1]])

    n_boundary_min = min(left_n_boundary)
    n_boundary_max = max(right_n_boundary)

    p_boundary_min = min(left_p_boundary)
    p_boundary_max = max(right_p_boundary)

    # Generate a dense grid of fixed-X arrays
    dense_arrays = {}
    for mu in mu_array:
        dense_p_array = []
        dense_n_array = []
        for X in X_array:
            pQCDX = pQCD(X)
            dense_p_array.append(pQCDX.pH(mu))
            dense_n_array.append(pQCDX.nH(mu))
        dense_arrays[mu] = (np.array(dense_p_array), np.array(dense_n_array))

    return {
        'X_array': X_array,
        'mu_array': mu_array,

        'p_boundary_arrays': p_boundary_arrays,
        'n_boundary_arrays': n_boundary_arrays,
        'mu_boundary_arrays': mu_boundary_arrays,

        'left_n_boundary': left_n_boundary,
        'right_n_boundary': right_n_boundary,
        'left_p_boundary': left_p_boundary,
        'right_p_boundary': right_p_boundary,

        'n_boundary_min': n_boundary_min,
        'n_boundary_max': n_boundary_max,
        'p_boundary_min': p_boundary_min,
        'p_boundary_max': p_boundary_max,

        'dense_arrays': dense_arrays
    }


def consistent_with_pqcd(eos, pqcd_region_dict):

    pressure = to_GeV_per_cubic_femtometre(eos.pressurec2)
    energy_density = to_GeV_per_cubic_femtometre(eos.energy_densityc2)
    number_density = to_nucleons_per_cubic_femtometre(eos.baryon_density)

    chemical_potential = (energy_density+pressure)/number_density

    # Interpolate over chemical potential
    interp_array = pqcd_region_dict['mu_array'][
        (min(chemical_potential) < pqcd_region_dict['mu_array']) &
        (max(chemical_potential) > pqcd_region_dict['mu_array'])
    ]
    pressure_interp = np.interp(interp_array, chemical_potential, pressure)
    number_density_interp = np.interp(
        interp_array, chemical_potential, number_density
    )

    if len(pressure_interp) == 0:
        return False

    # Perform a quick filter to remove EOSs that don't cross the min and max
    # number densities
    if (
        max(number_density_interp) < pqcd_region_dict['n_boundary_min'] or
        min(number_density_interp) > pqcd_region_dict['n_boundary_max']
    ):
        return False

    # Perform a quick filter to remove EOSs that don't cross the min and max
    # pressures
    if (
        max(pressure_interp) < pqcd_region_dict['p_boundary_min'] or
        min(pressure_interp) > pqcd_region_dict['p_boundary_max']
    ):
        return False

    inside_region_n = []
    inside_region_p = []
    inside_region_mu = []

    for n, p, mu in zip(
        number_density_interp, pressure_interp, pqcd_region_dict['mu_array']
    ):
        if (
            pqcd_region_dict['p_boundary_min'] < p
            < pqcd_region_dict['p_boundary_max']
        ):
            min_n = pqcd_region_dict['left_n_boundary'][
                np.argmin(np.abs(pqcd_region_dict['left_p_boundary']-p))
                ]
            max_n = pqcd_region_dict['right_n_boundary'][
                np.argmin(np.abs(pqcd_region_dict['right_p_boundary']-p))
                ]
            if min_n < n < max_n:
                inside_region_n.append(n)
                inside_region_p.append(p)
                inside_region_mu.append(mu)

    if len(inside_region_n) > 0:

        inside_region_n = np.array(inside_region_n)
        inside_region_p = np.array(inside_region_p)
        inside_region_mu = np.array(inside_region_mu)

        mu_start = min(inside_region_mu)
        mu_end = max(inside_region_mu)

        # Given the start and end values of mu for the EOS inside the region,
        # we want to see if the EOS passes through the surface defined by the
        # region. Assuming the EOS only crosses the surface once, we can simply
        # check if the EOS starts above the surface and ends below it, or vice
        # versa.

        # We want to "project" the start of the EOS onto the pQCD surface to
        # find the value of mu on the surface. This may be less than the EOS
        # value (in which case the EOS is "above" the surface) or greater than
        # the EOS value (in which case the EOS is "below" the surface).

        # To do this we use the dense arrays defined above. These are arrays of
        # p and n values for fixed mu. We find the closest (p,n) pair to the
        # EOS start point and use the corresponding mu value as the "projected"
        # mu value.

        n_start = inside_region_n[np.argmin(inside_region_mu)]
        p_start = inside_region_p[np.argmin(inside_region_mu)]

        min_delta = 10
        for mu, (dense_p_array, dense_n_array) in (
            pqcd_region_dict['dense_arrays'].items()
        ):
            delta = abs(
                n_start -
                dense_n_array[np.argmin(np.abs(dense_p_array-p_start))]
            )
            if delta < min_delta:
                min_delta = delta
                mu_start_projected = mu

        n_end = inside_region_n[np.argmax(inside_region_mu)]
        p_end = inside_region_p[np.argmax(inside_region_mu)]

        min_delta = 10
        for mu, (dense_p_array, dense_n_array) in (
            pqcd_region_dict['dense_arrays'].items()
        ):
            delta = abs(
                n_end - dense_n_array[np.argmin(np.abs(dense_p_array-p_end))]
            )
            if delta < min_delta:
                min_delta = delta
                mu_end_projected = mu

        # EOS starts above the surface and ends below it
        if (mu_start > mu_start_projected) and (mu_end < mu_end_projected):
            return True

        # EOS starts below the surface and ends above it
        elif (mu_start < mu_start_projected) and (mu_end > mu_end_projected):
            return True

        # The above does not consider the case of the EOS crossing the surface
        # an even number of times...

    return False
