import numpy as np

import pickle

from pqcd import pQCD
from scipy.stats import gaussian_kde


# The "maximised" pQCD likelihood, https://zenodo.org/records/7781233
# -------------------------------------------------------------------
# See also https://github.com/OKomoltsev/QCD-likelihood-function/tree/main
# The pQCD class, which the maximised class uses, has been moved to pqcd.py

def maximised_likelihood(e0, p0, n0, X, muH=2.6, cs2=1):
     	
	pQCDX = pQCD(X)
	
	mu0 = (e0 + p0) / n0
	pH = pQCDX.pH(muH)
	nH = pQCDX.nH(muH)
	Deltap = pH - p0
	pMin = cs2 / (1.0 + cs2) * (muH * (muH / mu0) ** (1. / cs2) - mu0) * n0
	pMax = cs2 / (1.0 + cs2) * (muH - mu0 * (mu0 / muH) ** (1. / cs2)) * nH
	nMax = nH * (mu0 / muH) ** (1. / cs2)
	
	tag = (pMin < Deltap < pMax) and (n0 < nMax)
    
	return tag


# The "marginalised" pQCD likelihood, https://zenodo.org/records/10592568
# -----------------------------------------------------------------------

class marginalised:
    
    def __init__(self, flag='conditioned'):
        
        if flag == 'conditioned':
            filename = '../data/eos-extensions/eos_extensions_s-G-1p25-0p25_l-U-1-20_meancs2-G-0.3-0.3_pQCD-25-40.pickle'
        elif flag == 'prior':
            filename = '../data/eos-extensions/eos_extensions_s-G-1p25-0p25_l-U-1-20_meancs2-G-0.3-0.3.pickle'
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
    
    def likelihood(self): 
         
        nL_tab = np.linspace(0,40,99*10+1)*0.16
        dn = nL_tab[1]-nL_tab[0]
        nL_tab = nL_tab[int(1.*0.16/dn):int(35.*0.16/dn)]
        
        kernel_tab = [self.weight_kernel_fixed_n(nL) for nL in nL_tab]

        def interp_kernels(e0, p0, n0, kernelTAB=kernel_tab):
            
            if n0 > 35.*0.16:
                raise ValueError('nL must be < 35*0.16')
            if n0 < 1.*0.16:
                raise ValueError('nL must be > 1*0.16')

            cnt = int((n0-nL_tab[0])/dn)
            # now nLTAB[cnt] < N and nLTAB[cnt+1] > N
            
            return np.interp(
                n0, 
                [nL_tab[cnt], nL_tab[cnt+1]], 
                [kernelTAB[cnt]([e0, p0])[0], kernelTAB[cnt+1]([e0, p0])[0]]
                )
        
        return interp_kernels