import numpy as np

from muon_sim import mcmc


class MuonSample:
	X = "x0"
	Y = "y0"
	Z = "z0"
	DX = "dx"
	DY = "dy"
	DZ = "dz"
	def __init__(self, nmuons):
		self.param = dict()
		x, y = mcmc.random_circle(nmuons, 0.4)
		self.param[self.X] = x
		self.param[self.Y] = y
		self.param[self.Z]  = np.random.uniform(0, 0.6, nmuons)
		phi = np.random.uniform(0, 2 * np.pi, nmuons)
		pdf = mcmc.pdf_normed(lambda x: np.exp(- 0.1 * x), (0, np.pi / 2))
		thetha = mcmc.mcmc(pdf, nmuons, 1024, 0.1)
		self.param[self.DX] = np.sin(thetha) * np.cos(phi)
		self.param[self.DY] = np.sin(thetha) * np.sin(phi)
		self.param[self.DZ] = np.cos(thetha)
