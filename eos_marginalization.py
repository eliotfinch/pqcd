import numpy as np
import pickle
from scipy.stats import gaussian_kde
from bisect import bisect

class eos_marginalization:
    def __init__(self, flag='conditioned'):
        if flag == 'conditioned':
            filename = 'eos_extensions/eos_extensions_s-G-1p25-0p25_l-U-1-20_meancs2-G-0.3-0.3_pQCD-25-40.pickle'
        elif flag == 'prior':
            filename = 'eos_extensions/eos_extensions_s-G-1p25-0p25_l-U-1-20_meancs2-G-0.3-0.3.pickle'
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