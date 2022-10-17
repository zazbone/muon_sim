"""Monte Carlo simulation of an atmospheric muon detector"""

__version__ = "0.1"


import numpy as np
import matplotlib.pylab as plt
from scipy.integrate import simpson


EPS = np.finfo(float).eps


def pdf_normed(pdf, xlim):
	x = np.linspace(*xlim, 1024)
	NORM = simpson(x, pdf(x))
	def prior(x):
		return ((xlim[0] < x) & (x < xlim[1])) + EPS
	def normed(x):
		return pdf(x) / NORM * prior(x)
	return normed

def mcmc(pdf, nsample, nit, L):
    xi = np.full(nsample, 0.5)
    for _ in range(nit):
        xp = np.random.uniform(-L, L, nsample) + xi
        alpha = pdf(xp) / pdf(xi)
        mask = np.random.uniform(0, 1, nsample) <= alpha
        xi[mask] = xp[mask]
    return xi