import numpy as np

import pickle

from scipy.stats import gaussian_kde
from bisect import bisect


# "Maximised" pQCD likelihood, https://zenodo.org/records/7781233
# ---------------------------------------------------------------

GeV3_to_fm3 = 1.0e3/1.9732705**3

# definition of auxiliary functions

def PNLO(a_s):
	return 1. - 0.637*a_s

def PNNLO(a_s,X):
	return -a_s**2*(-1.831 + 0.304*np.log(a_s)) + a_s**2*(-2.706 - 0.912*np.log(X))

def PN3LO(a_s):
	return 0.484816*a_s**3

def alpha_s(mu,X):
	numerator = 4*np.pi*(1. - (64.*np.log(np.log(0.777632*mu**2*X**2)))/(81.*np.log(0.777632*mu**2*X**2)))
	denominator = (9.*np.log(0.777632*mu**2*X**2))
	return numerator/denominator

def das_dmu(mu,X):
	numerator = -2.20644 - 2.79253*np.log(0.777632*mu**2*X**2) + 4.41288*np.log(np.log(0.777632*mu**2*X**2))
	denominator = mu*(np.log(0.777632*mu**2*X**2))**3
	return numerator/denominator

def d2as_dmu2(mu,X):
	numerator1 = 22.0644 + 2.79253*(np.log(0.777632*mu**2*X**2))**2 - 26.4773*np.log(np.log(0.777632*mu**2*X**2))
	numerator2 = np.log(0.777632*mu**2*X**2)*(13.3765 - 4.41288*np.log(np.log(0.777632*mu**2*X**2)))
	denominator = mu**2*(np.log(0.777632*mu**2*X**2))**4
	return (numerator1+numerator2)/denominator

def dp_das(a_s,X):
	dPNLO = -0.637
	dPNNLO = a_s*(-2.054 - 0.608*np.log(a_s) - 1.824*np.log(X))
	dPN3LO = 1.45445*a_s**2 
	return dPNLO + dPNNLO + dPN3LO

def d2p_das2(a_s,X):
	d2PNNLO = -2.662 - 0.608*np.log(a_s) - 1.824*np.log(X)
	d2PN3LO = 2.9089*a_s 
	return d2PNNLO + d2PN3LO

def pFD(mu):
	return (mu)**4/(108*np.pi**2)

def dpFD(mu):
	return mu**3/(27*np.pi**2)

def d2pFD(mu):
	return mu**2/(9*np.pi**2)

def n_dens_QCD(mu,X): # fm-3

		a_s = alpha_s(mu,X)
		p_as = (PNLO(a_s) + PNNLO(a_s,X) + PN3LO(a_s))

		return (dp_das(a_s,X)*das_dmu(mu,X)*pFD(mu) + p_as*dpFD(mu))*GeV3_to_fm3

def speed2_QCD(mu,X):

		a_s = alpha_s(mu,X)
		p_as = (PNLO(a_s) + PNNLO(a_s,X) + PN3LO(a_s))

		dn_dmu1 = pFD(mu)*(d2p_das2(a_s,X)*(das_dmu(mu,X))**2 + dp_das(a_s,X)*d2as_dmu2(mu,X))
		dn_dmu2 = 2.*dp_das(a_s,X)*das_dmu(mu,X)*dpFD(mu) + p_as * d2pFD(mu)

		return n_dens_QCD(mu,X)/(mu*GeV3_to_fm3*(dn_dmu1+dn_dmu2))

def pressure_QCD(mu, X): # MeV/fm-3

		a_s = alpha_s(mu, X)

		return (PNLO(a_s) + PNNLO(a_s, X) + PN3LO(a_s))*pFD(mu)*GeV3_to_fm3*1.e3

# main pQCD class
    
class pQCD:

	def __init__(self, X):

		self.X = 2.*X

	def pressure(self,mu): #GeV/fm3
		a_s = alpha_s(mu,self.X)
		return (PNLO(a_s) + PNNLO(a_s,self.X) + PN3LO(a_s))*pFD(mu)*GeV3_to_fm3

	def number_density(self,mu): # fm-3
		a_s = alpha_s(mu,self.X)
		p_as = (PNLO(a_s) + PNNLO(a_s,self.X) + PN3LO(a_s))
		return (dp_das(a_s,self.X)*das_dmu(mu,self.X)*pFD(mu) + p_as*dpFD(mu))*GeV3_to_fm3

	def edens(self,mu): #GeV/fm3
		return -self.pressure(mu)+mu*self.number_density(mu)

	def speed2(self,mu):
		a_s = alpha_s(mu,self.X)
		p_as = (PNLO(a_s) + PNNLO(a_s,self.X) + PN3LO(a_s))

		dn_dmu1 = pFD(mu)*(d2p_das2(a_s,self.X)*(das_dmu(mu,self.X))**2 + dp_das(a_s,self.X)*d2as_dmu2(mu,self.X))
		dn_dmu2 = 2.*dp_das(a_s,self.X)*das_dmu(mu,self.X)*dpFD(mu) + p_as * d2pFD(mu)

		return self.number_density(mu)/(mu*GeV3_to_fm3*(dn_dmu1+dn_dmu2))

	def constraints(self, e0, p0, n0, muQCD = 2.6, cs2=1): 

		mu0 = (e0 + p0) / n0
		pQCD = self.pressure(muQCD)
		nQCD = self.number_density(muQCD)
		deltaP = pQCD - p0
		pMin = cs2 / (1.0 + cs2) * (muQCD * (muQCD / mu0) ** (1. / cs2) - mu0) * n0
		pMax = cs2 / (1.0 + cs2) * (muQCD - mu0 * (mu0 / muQCD) ** (1. / cs2)) * nQCD
		nMax = nQCD * (mu0 / muQCD) ** (1. / cs2)

		tag = (pMin < deltaP < pMax) and (n0 < nMax)
		return tag


# The "marginalised" pQCD likelihood, https://zenodo.org/records/10592568
# -----------------------------------------------------------------------
	
class eos_marginalization:
    def __init__(self, flag='conditioned'):
        if flag == 'conditioned':
            filename = 'eos-extensions/eos_extensions_s-G-1p25-0p25_l-U-1-20_meancs2-G-0.3-0.3_pQCD-25-40.pickle'
        elif flag == 'prior':
            filename = 'eos-extensions/eos_extensions_s-G-1p25-0p25_l-U-1-20_meancs2-G-0.3-0.3.pickle'
        else:
            raise ValueError("Flag must be 'conditioned' or 'prior'")

        with open(filename, "rb") as f:
            self.eos_extensions = pickle.load(f)

        self.eos_extensions['n'] = (self.eos_extensions['p']+self.eos_extensions['e'])/self.eos_extensions['mu']

    def weight_kernel_fixed_n(self, n0):
        eosn = self.eos_extensions.n
        eose = self.eos_extensions.e
        eosp = self.eos_extensions.p

        eps_s = [np.interp(n0,nn[::-1],ee[::-1]) for (nn,ee) in zip(eosn, eose)]
        p_s   = [np.interp(n0,nn[::-1],pp[::-1]) for (nn,pp) in zip(eosn,eosp)]

        values = np.array([eps_s, p_s])

        return gaussian_kde(values)

    def marg_QCD_likelihood(self): 
        
        eosn = self.eos_extensions.n

        nL_tab = np.linspace(1,35,100)*0.16
        kernel_tab = [self.weight_kernel_fixed_n(nL) for nL in nL_tab]

        def interp_kernels(e0, p0, n0, nLTAB = nL_tab, kernelTAB = kernel_tab):
            if n0 > 35.*0.16:
                raise ValueError('n0 must be < 35*0.16')
            if n0 < 1.*0.16:
                raise ValueError('n0 must be > 1*0.16')

            cnt = bisect(nLTAB, n0) - 1 # now nLTAB[cnt] < N and nLTAB[cnt-1] > N

            return np.interp(n0, 
                             kernelTAB[cnt]([e0, p0]), 
                             kernelTAB[cnt+1]([e0, p0]))

        return interp_kernels