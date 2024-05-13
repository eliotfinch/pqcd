import numpy as np

from scipy.integrate import cumulative_trapezoid

def epsilon_func(mu, n, p):
    return -p + mu*n

def pressure_integral(mu, n, pL):
    return pL + cumulative_trapezoid(n, mu)

# The following functions are taken from 
# https://zenodo.org/records/7781233

# See also 
# https://github.com/OKomoltsev/QCD-likelihood-function/tree/main

GeV3_to_fm3 = 1.0e3/1.9732705**3

def PNLO(a_s):
	return 1. - 0.637*a_s

def PNNLO(a_s, X):
	return -a_s**2*(-1.831 + 0.304*np.log(a_s)) + a_s**2*(-2.706 - 0.912*np.log(X))

def PN3LO(a_s):
	return 0.484816*a_s**3

def alpha_s(mu, X):
	numerator = 4*np.pi*(1. - (64.*np.log(np.log(0.777632*mu**2*X**2)))/(81.*np.log(0.777632*mu**2*X**2)))
	denominator = (9.*np.log(0.777632*mu**2*X**2))
	return numerator/denominator

def das_dmu(mu, X):
	numerator = -2.20644 - 2.79253*np.log(0.777632*mu**2*X**2) + 4.41288*np.log(np.log(0.777632*mu**2*X**2))
	denominator = mu*(np.log(0.777632*mu**2*X**2))**3
	return numerator/denominator

def d2as_dmu2(mu, X):
	numerator1 = 22.0644 + 2.79253*(np.log(0.777632*mu**2*X**2))**2 - 26.4773*np.log(np.log(0.777632*mu**2*X**2))
	numerator2 = np.log(0.777632*mu**2*X**2)*(13.3765 - 4.41288*np.log(np.log(0.777632*mu**2*X**2)))
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

	def pH(self, mu): # GeV/fm^3
		a_s = alpha_s(mu,self.X)
		return (PNLO(a_s) + PNNLO(a_s,self.X) + PN3LO(a_s))*pFD(mu)*GeV3_to_fm3

	def nH(self, mu): # 1/fm^3
		a_s = alpha_s(mu,self.X)
		p_as = (PNLO(a_s) + PNNLO(a_s,self.X) + PN3LO(a_s))
		return (dp_das(a_s,self.X)*das_dmu(mu,self.X)*pFD(mu) + p_as*dpFD(mu))*GeV3_to_fm3

	def epsilonH(self, mu): # GeV/fm^3
		return epsilon_func(mu, self.nH(mu), self.pH(mu))

	def cs2H(self, mu):
		a_s = alpha_s(mu,self.X)
		p_as = (PNLO(a_s) + PNNLO(a_s,self.X) + PN3LO(a_s))

		dn_dmu1 = pFD(mu)*(d2p_das2(a_s,self.X)*(das_dmu(mu,self.X))**2 + dp_das(a_s,self.X)*d2as_dmu2(mu,self.X))
		dn_dmu2 = 2.*dp_das(a_s,self.X)*das_dmu(mu,self.X)*dpFD(mu) + p_as * d2pFD(mu)

		return self.nH(mu)/(mu*GeV3_to_fm3*(dn_dmu1+dn_dmu2))