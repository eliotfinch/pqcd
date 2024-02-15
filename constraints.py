import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import cumulative_trapezoid

# The "maximised" pQCD likelihood
from pQCD import pQCD
def pQCD_likelihood(e, p, n, X):
    pQCDX = pQCD(X)
    return int(pQCDX.constraints(e0=e,p0=p,n0=n))

# The "marginalised" pQCD likelihood
from eos_marginalization import eos_marginalization
eos_marginalization_conditioned = eos_marginalization(flag='conditioned')
pQCD_likelihood_marg = eos_marginalization_conditioned.marg_QCD_likelihood()

def epsilon(mu, n, p):
    return -p + mu*n

def p(mu, n, pL):
    return pL + cumulative_trapezoid(n, mu)


class pQCD_constraints:

    def __init__(self, muL, nL, pL, muH, nH, pH):
        """
        Initialize the pQCD_constraints class. Functions taken from Komoltsev 
        & Kurkela 2022, arXiv:2111.05350.
        
        Parameters
        ----------
        muL, nL, pL : float
            Predicted values of the baryon chemical potential [GeV], baryon 
            number density [1/fm^3], and pressure [GeV/fm^3] at low density.
        
        muH, nH, pH : float
            Predicted values of the baryon chemical potential [GeV], baryon 
            number density [1/fm^3], and pressure [GeV/fm^3] at high density.
        """
        self.muL = muL
        self.nL = nL
        self.pL = pL
        self.muH = muH
        self.nH = nH
        self.pH = pH

        self.Deltap = pH - pL
        self.muc = np.sqrt(
            (muL*muH*(muH*nH - muL*nL - 2*self.Deltap))/(muL*nH - muH*nL)
            )
        
        self.epsilonL = epsilon(muL, nL, pL)
        self.epsilonH = epsilon(muH, nH, pH)
        
        self.nmax = np.vectorize(self.nmax_scalar)
        self.nmin = np.vectorize(self.nmin_scalar)

        self.pmax = np.vectorize(self.pmax_scalar)

    def nmin_scalar(self, mu):
        """
        Returns the minimum allowed value of the baryon number density at a
        given baryon chemical potential.
        """
        if self.muL <= mu <= self.muc:
            return self.nL*mu/self.muL
        
        elif self.muc < mu <= self.muH:
            numerator = mu**3*self.nH - mu*self.muH*(self.muH*self.nH - 2*self.Deltap)
            denominator = (mu**2 - self.muL**2)*self.muH
            return numerator/denominator
        
        else:
            raise ValueError('mu is outside the range [muL, muH]')
        
    def nmax_scalar(self, mu):
        """
        Returns the maximum allowed value of the baryon number density at a 
        given baryon chemical potential.
        """
        if self.muL <= mu < self.muc:
            numerator = mu**3*self.nL - mu*self.muL*(self.muL*self.nL + 2*self.Deltap)
            denominator = (mu**2 - self.muH**2)*self.muL
            return numerator/denominator
        
        elif self.muc <= mu <= self.muH:
            return self.nH*mu/self.muH
        
        else:
            raise ValueError('mu is outside the range [muL, muH]')
        
    def nc(self, mu):
        """
        The special EOS for which the speed of sound is equal to the speed of
        light throughout the whole region.
        """
        return (self.nmin(self.muH)*mu)/self.muH

    def pmin(self, mu):
        """
        Returns the minimum allowed value of the pressure at a given baryon
        chemical potential.
        """
        return self.pL + ((mu**2 - self.muL**2)/(2*mu))*self.nmin(mu)
    
    def pmax_scalar(self, mu, n):
        """
        Returns the maximum allowed value of the pressure at a given baryon
        chemical potential and baryon number density.
        """
        if n < self.nc(mu):
            return self.pL + ((mu**2 - self.muL**2)/(2*mu))*n
        
        else:
            return self.pH - ((self.muH**2 - mu**2)/(2*mu))*n
        
    def epsilon_min(self, mu):
        """
        Returns the minimum allowed value of the energy density at a given 
        baryon chemical potential.
        """
        return -self.pmax(mu, self.nmin(mu)) + mu*self.nmin(mu)
    
    def epsilon_max(self, mu):
        """
        Returns the maximum allowed value of the energy density at a given 
        baryon chemical potential.
        """
        return -self.pmin(mu) + mu*self.nmax(mu)
    
    def plot_mu_n(self, mu_array):
        """
        Plots the allowed region of the baryon number density as a function of 
        the baryon chemical potential.

        Parameters
        ----------
        mu_array : array-like
            An array of baryon chemical potential values [GeV].
        """
        fig, ax = plt.subplots()

        ax.plot(mu_array, self.nmin(mu_array), c='C0', label=r'$n_\mathrm{min}$')
        ax.plot(mu_array, self.nmax(mu_array), c='C1', label=r'$n_\mathrm{max}$')

        ax.axvline(self.muc, ls='--', c='C2', label=r'$\mu_\mathrm{c}$')
        ax.plot(mu_array, self.nc(mu_array), ls='--',  c='C3', label='$n_\mathrm{c}$')

        ax.plot(self.muL, self.nL, 'o', c='C4', label=r'$(\mu_\mathrm{L}, n_\mathrm{L})$')
        ax.plot(self.muH, self.nH, 'o', c='C5', label=r'$(\mu_\mathrm{H}, n_\mathrm{H})$')

        ylim = [0, ax.get_ylim()[1]]

        ax.fill_between(mu_array, self.nmax(mu_array), ylim[1], color='k', alpha=0.2)
        ax.fill_between(mu_array, self.nmin(mu_array), ylim[0], color='k', alpha=0.2)

        ax.set_xlabel(r'$\mu$ [GeV]')
        ax.set_ylabel(r'$n$ [1/fm$^3$]')

        ax.legend()

        ax.set_xlim(self.muL, self.muH)
        ax.set_ylim(ylim)

        return fig, ax
    
    def plot_epsilon_p(self, mu_array, log=True):
        """
        Plots the allowed region of the pressure as a function of the energy 
        density.

        Parameters
        ----------
        mu_array : array-like
            An array of baryon chemical potential values [GeV].

        log : bool, optional
            If True, the x- and y-axes will be logarithmically scaled. 
            Default is True.
        """
        fig, ax = plt.subplots()

        if log:
            ax.set_xscale('log')
            ax.set_yscale('log')

        ax.plot(
            self.epsilon_min(mu_array), 
            self.pmax(mu_array, self.nmin(mu_array)), 
            c='C0',
            label=r'$\epsilon_\mathrm{min}$',
            )
        ax.plot(
            self.epsilon_max(mu_array), 
            self.pmin(mu_array), 
            c='C1',
            label=r'$\epsilon_\mathrm{max}$',
            )

        ax.plot(
            epsilon(mu_array, self.nc(mu_array), self.pmax(mu_array, self.nc(mu_array)))[1:], 
            p(mu_array, self.nc(mu_array), self.pL), 
            ls='--',
            c='C3',
            label=r'$n_c$'
            )

        ax.plot(self.epsilonL, self.pL, 'o', c='C4', label=r'$(\epsilon_\mathrm{L}, p_\mathrm{L})$')
        ax.plot(self.epsilonH, self.pH, 'o', c='C5', label=r'$(\epsilon_\mathrm{H}, p_\mathrm{H})$')

        xlim = ax.get_xlim()

        ax.fill_betweenx(
            self.pmax(mu_array, self.nmin(mu_array)), 
            self.epsilon_min(mu_array), 
            xlim[0], 
            color='k', 
            alpha=0.2
            )
        
        ax.fill_betweenx(
            self.pmin(mu_array), 
            self.epsilon_max(mu_array), 
            xlim[1], 
            color='k', 
            alpha=0.2
            )

        ax.set_xlabel(r'$\epsilon$ [GeV/fm$^3$]')
        ax.set_ylabel(r'$p$ [GeV/fm$^3$]')

        ax.set_xlim(xlim)
        ax.set_ylim(self.pL, self.pH)

        ax.legend()

        return fig, ax