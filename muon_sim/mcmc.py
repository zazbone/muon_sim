import numpy as np
import numba as nb
from scipy.integrate import quad


EPS = np.finfo(float).eps


nb.njit(parallel=True)
def random_circle(N, R, C=(0, 0)):
    """
    Generate N points uniformly distributed within a circle of radius R centered at C.

    Parameters
    ----------
    N: (int)
        The number of points to generate.
    R: (float)
        The radius of the circle.
    C: (tuple)
        The coordinates of the center of the circle. Default is (0, 0).

    Returns
    -------
    x: (ndarray)
        An array of N x-coordinates for the generated points.
    y: (ndarray)
        An array of N y-coordinates for the generated points.
    """
    r = R * np.sqrt(np.random.random(N))
    theta = np.random.uniform(0, 2 * np.pi, N)
    x = r * np.cos(theta) + C[0]
    y = r * np.sin(theta) + C[1]
    return x, y


def pdf_normed(pdf, xlim: tuple[float, float]):
    """
    Normalize the probability density function (PDF) on a given range by the integral of the PDF on this range.
    The function also sets the return values to zero outside of the given range.

    Parameters
    ----------
    pdf : Function
        Probability density function. With one argument and a return value
        The pdf must be positive defined on the given interval

    xlim : tuple[float, float]
        Contains the minimal and maximal value of the definition range of the normed pdf.

    Returns
    -------
    Function
        Normalized probability density function. Support numpy array and scalar value.
    """
    NORM, _err = quad(pdf, *xlim)

    @nb.njit(parallel=True)
    def prior(x):
        mask = (xlim[0] <= x) & (x <= xlim[1])
        return np.where(mask, 1, EPS)

    @nb.njit(parallel=True)
    def normed(x):
        return pdf(x) / NORM * prior(x)

    return normed


@nb.jit()
def walk(x, nit, sigma, pdf, prior=None, keep_all=False):
    """
    Execute nit Markov Chain Monte Carlo (MCMC) steps on the sample x with pdf as the model for the desired distribution.
    It is recommended to begin with a uniform sample for x and provide enough steps for the algorithm to converge.
    Set keep_all to True if you want to keep all intermediate steps (only use this if the sample has already converged).

    Parameters
    ----------
    x : numpy ndarray
        The initial value of the sample (walkers)
        If it had more than 1 dim, it will be flattened
    nit : int
        Number of steps of the mcmc algorith
    sigma:
        The standard deviation of the mcmc steps values distribution
    pdf : Function
        The probability density function that the sample should converge to.
    prior : Function
        And optionnal prior function for the algorithm
        By default prior is set to 1
    keep_all : bool
        If True, all steps of the MCMC method will be kept and returned.

    Returns
    -------
    Numpy ndarray :
        If keep_all, return a 2 dim array containing all the step off the mcmc methode in is row
        Otherwise, only the final state of the walkers is returned.
    """
    if prior is None:
        @nb.njit(parallel=True)
        def prior(_):
            return 1

    # Fattern the sample if it have more than 1 dimension
    xi = x.flatten()
    n = len(xi)
    if keep_all:
        xall = np.zeros((nit, n))
    for i in range(nit):
        step = np.random.normal(0, np.abs(sigma), n)
        xp = step + xi
        # Avoid div by zero with EPS
        alpha = (pdf(xp) * prior(xp) + EPS) / (pdf(xi) * prior(xi) + EPS)
        mask = np.random.uniform(0, 1, n) <= alpha
        xi[mask] = xp[mask]
        if keep_all:
            xall[i] = xi
    if keep_all:
        return xall
    return xi


def pdf_normed2D(pdf, xlim, ylim):
    """Normalize a 2D probability density function by computing the integral over xlim and ylim

    Parameters
    ----------
    pdf : Callable[x: ndarray, y: ndarray] -> ndarray
        2D probability density function
    xlim : tuple[float, float]
        Contains the minimal and maximal value of the definition x range of the normed pdf.
        Value outside will be set with a prior = 0
    ylim : tuple[float, float]
        Contains the minimal and maximal value of the definition y range of the normed pdf.
        Value outside will be set with a prior = 0

    Returns
    -------
    Callable[x: ndarray, y: ndarray] -> ndarray
        Normalized pdf
    """
    pass


def walk2D(x, y, nit, sigma, pdf, prior=None, keep_all=False):
    """Walker for 2D random variables distribution

    Parameters
    ----------
    x, y : ndarray
        Initial state of the x and y walkers
        If ndarrays have more than 1 dim, they will be flatten
    nit : int
        Number of step of the mcmc algorith
    sigma : tuple[float, float]
        The standard deviation of the mcmc steps values distribution for x and y
        sigma[0] = sigma_x, sigma[1] = sigma_y
    pdf : Callable[x: ndarray, y: ndarray] -> ndarray
        The 2D probability density function to wich the sample should converge
    prior : Callable[x: ndarray, y: ndarray] -> ndarray, optional
        And optionnal prior function for the algorithm
        By default prior is set to 1
    keep_all : bool, optional
        If true the all the set of the mcmc methode will be keeped and returned

    Returns
    -------
    tuple[ndarray, ndarray]
        (x, y)
        If keep_all, 2 dim arrays containing all the step off the mcmc methode in is row
        else only the final state of the walkers
    """
    pass
