from muon_sim import mcmc
import numpy as np
from itertools import count


class MCMCSampler:
    def __init__(self, pdf, lim, nwalkers):
        """One dimension mcmc sampler

        Use the given probability density function to generate random variables.
        The convergence and best parameters are automatically gessed at initialisation

        Parameters
        ----------
        pdf : Callable[ndarray] -> ndarray
            Probability density function of the desired random variable distribution.
            Don't need to be normalized
        lim : tuple[float, float]
            Limite of definition of the pdf.
            Value outside will be set with a prior = 0
        nwalkers : int
            size of the walkers array
        """
        self.pdf = mcmc.pdf_normed(pdf, lim)
        self.walkers = np.random.uniform(*lim, nwalkers)
        self.sigma = (lim[1] - lim[0]) / 20
        self.sigma = self.fit_sigma()  # First fit before convergence
        self.converge()
        self.sigma = self.fit_sigma()
        self.ncor = 1
        self.ncor = self.fit_ncor()
    
    def step(self, n=1):
        """Run n mcmc step and return nth walkers state
        /!\\ do not take correlation in account, use self.sample if you want to generate samples

        Parameters
        ----------
        n : int, optional
            number of mcmc steps, by default 1

        Returns
        -------
        ndarray
            nth walkers state
        """
        return mcmc.walk(self.walkers, n, self.sigma, self.pdf)
    
    def sample(self, n):
        """Generate n * nwalkers random variables
        All walkers states are decorrelated 

        Parameters
        ----------
        n : int
            number of decorrelated walkers states

        Returns
        -------
        ndarray
            Sample generated, with shape = (n, nwalkers)
        """
        samp = np.zeros((n, self.walkers.shape[0]))
        for i in range(n):
            self.walkers = self.step(self.ncor)
            samp[i, :] = self.walkers.copy()
        return samp
    
    def converge(self):
        # TODO: Find a better check for convergence
        self.walkers = self.step(1024)

    def fit_sigma(self):
        # TODO: Not a dumb description plz
        """Find the best sigma parameter for walk step size
        The sigma is define as the sigma parameter for muon_sim.mcmc.walk function with the acceptance rate nearest 60 %

        Returns
        -------
        float
            Best sigma parameter for walk step size

        Raises
        ------
        RuntimeError
            The best sigma is defined with a tolerence, if it cannot be reached in 1024 step the function fail
        """
        X = self.walkers
        N = self.walkers.shape[0]
        sigma = self.sigma
        def walk(sig):
            return mcmc.walk(X, 1, sig, self.pdf)

        def y(sig):
            return np.sum(np.isclose(X, walk(sig))) / N - 0.6
        
        D = 0.05
        i = 0
        while np.abs(y(sigma)) > 0.05:
            if y(sigma) < 0:
                sigma += D
            else:
                sigma -= D
            i += 1
            if i > 1024:
                raise RuntimeError("Failed to make sigma converge in a resonable time")
        return sigma
        
    def fit_ncor(self):
        """Gest the minimum mcmc step to reach a corelation bellow 0.05

        Returns
        -------
        int
            minimum step to reduce correlation between mcmc steps bellow 0.05

        Raises
        ------
        RuntimeError
            If low correlation is not reach in 1024 steps
        """        """"""
        for i in range(1024):
            x = self.step(1)
            y = self.step(i)
            corr = np.corrcoef(x, y)[0, 1]
            if corr < 0.05:
                return i

        raise RuntimeError("Failed to reach low correlation in a resonable time")
