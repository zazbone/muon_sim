import numpy as np
from scipy.integrate import simpson, nquad


EPS = np.finfo(float).eps


def random_circle(N, R, C=(0, 0)):
    """
    Uniformaly generate point in a given circle
    """
    r = R * np.sqrt(np.random.random(N))
    theta = np.random.uniform(0, 2 * np.pi, N)
    x = r * np.cos(theta) + C[0]
    y = r * np.sin(theta) + C[1]
    return x, y

# TODO: check spelling
def pdf_normed(pdf, xlim: tuple[float, float]):
    """
    Normalise the probability density function on a given range by the integral on this range.
    And set the return values of this function to zero outside of the range.

    Parameters
    ----------
    pdf : Function
        Probability density function. With one argument and a return value,
        both must be numpy ndarray (requirered for the integral)
    xlim : tuple[float, float]
        Contains the minimal and maximal value of the definition range of the normed pdf.

    Returns
    -------
    Function
        Normalized probability density function. Support numpy array and scalar value.
    """
    x = np.linspace(*xlim, 1024)
    NORM = simpson(x, pdf(x))
    def prior(x):
        return ((xlim[0] < x) & (x < xlim[1])) + EPS
    def normed(x):
        return pdf(x) / NORM * prior(x)
    return normed


# TODO: check spelling
def walk(x, nit, sigma, pdf, prior=None, keep_all=False):
    """
    Execute nit mcmc step on the x sample (walkers) with pdf as model for the desired distribution.
    Its recommended to begin with an uniform sample for x and give enouth step for the algorithm to converge.
    Se keep_all to True if you want to keep all intermediate step (Use it only if the sample had already converge)

    Parameters
    ----------
    x : numpy ndarray
        The initial value of the sample (walkers)
        If it had more than 1 dim, it wil be flatten
    nit : int
        Number of step of the mcmc algorith
    sigma:
        The standard deviation of the mcmc steps values distribution
    pdf : Function
        The probability density function to with the sample should converge
    prior : Function
        And optionnal prior function for the algorithm
        By default prior is set to 1
    keep_all : bool
        If true the all the set of the mcmc methode will be keeped and returned

    Returns
    -------
    Numpy ndarray :
        If keep_all, 2 dim array containing all the step off the mcmc methode in is row
        else only the final state of the walkers
    """
    if prior is None:
        prior = lambda _: 1

    # Fattern the sample if it have more than 1 dimension
    xi = x.flatten()
    n = len(xi)
    if keep_all:
        xall = np.zeros((nit, n))
    for i in range(nit):
        step = np.random.normal(0, sigma, n)
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

def pdf_normedND(pdf, lim: list[tuple[float, float]], *args):
    """
    Normalise the probability ndim density function on a given range by the integral on this range.
    And set the return values of this function to zero outside of the range.

    Parameters
    ----------
    pdf : Function
        Probability density function. With one argument and a return value,
        both must be numpy ndarray (requirered for the integral)
    lim : tuple[float, float]
        Contains the minimal and maximal value of the definition range of the normed pdf for each dim.
    *args :
        Additionnal constant arguments requirered by the pdf function 

    Returns
    -------
    Function
        Normalized probability density function. Support numpy array and scalar value.
    """
    NORM, _ = nquad(pdf, lim, args)
    def prior(X):
        cond = np.full(True, len(X[0]))
        for i, x in enumerate(X):
            cond = (lim[i][0] < x) & (x < lim[i][1]) & cond
        return cond + EPS
    def normed(*X):
        return pdf(*X, *args) / NORM * prior(X)
    return normed


# TODO: check spelling, check doc duplication
def walkND(X, nit, sigma, pdf, prior=None, keep_all=False):
    """
    Execute nit mcmc step on the x sample (walkers) with pdf as model for the desired distribution.
    Its recommended to begin with an uniform sample for x and give enouth step for the algorithm to converge.
    Se keep_all to True if you want to keep all intermediate step (Use it only if the sample had already converge)

    Parameters
    ----------
    x : numpy ndarray
        The initial value of the sample (walkers)
        If it had more than 1 dim, it wil be flatten
    nit : int
        Number of step of the mcmc algorith
    sigma:
        The standard deviation of the mcmc steps values distribution
    pdf : Function
        The probability density function to with the sample should converge
    prior : Function
        And optionnal prior function for the algorithm
        By default prior is set to 1
    keep_all : bool
        If true the all the set of the mcmc methode will be keeped and returned

    Returns
    -------
    Numpy ndarray :
        If keep_all, 2 dim array containing all the step off the mcmc methode in is row
        else only the final state of the walkers
    """
    if prior is None:
        prior = lambda _: 1

    # Fattern the sample if it have more than 1 dimension
    xi = x.flatten()
    n = len(xi)
    if keep_all:
        xall = np.zeros((nit, n))
    for i in range(nit):
        step = np.random.normal(0, sigma, n)
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