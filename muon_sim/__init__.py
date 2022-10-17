"""Monte Carlo simulation of an atmospheric muon detector"""

__version__ = "0.1"


import numpy as np
from scipy.integrate import simpson


EPS = np.finfo(float).eps


class MuonSample:
	X = "x0"
	Y = "y0"
	Z = "z0"
	DX = "dx"
	DY = "dy"
	DZ = "dz"
	def __init__(self, nmuons):
		self.param = dict()
		x, y = random_circle(nmuons, 0.4)
		self.param[self.X] = x
		self.param[self.Y] = y
		self.param[self.Z]  = np.random.uniform(0, 0.6, nmuons)
		phi = np.random.uniform(0, 2 * np.pi, nmuons)
		pdf = mcmc.pdf_normed(lambda x: np.exp(- 0.1 * x), (0, np.pi / 2))
		thetha = mcmc.mcmc(pdf, nmuons, 1024, 0.1)
		self.param[self.DX] = np.sin(thetha) * np.cos(phi)
		self.param[self.DY] = np.sin(thetha) * np.sin(phi)
		self.param[self.DZ] = np.cos(thetha)


def random_circle(N, R, C=(0, 0)):
    """
    Uniformaly generate point in a given circle
    """
    r = R * np.sqrt(np.random.random(N))
    theta = np.random.uniform(0, 2 * np.pi, N)
    x = r * np.cos(theta) + C[0]
    y = r * np.sin(theta) + C[1]
    return x, y


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