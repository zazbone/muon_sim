from ward import test, each
from utils import cst, linear, poly
from muon_sim.mcmc import pdf_normed
import numpy as np
from numpy.testing import assert_allclose
from numpy.random import uniform

functions = [
    lambda x, *_: np.sin(x),
    lambda x, a, *_: cst(x, a),
    lambda x, a, b, *_: linear(x, a, b),
    lambda x, a, b, c, *_: poly(x, [a, b, c], [2, 1, 0]),
    lambda x, a, *_: np.exp(a * x),
]

prob_dens = [
    lambda x, *_: np.sin(x) / (1 - np.cos(1)),
    lambda x, a, *_: cst(x, 1),
    lambda x, a, b, *_: linear(x, a, b) / (0.5 * a + b),
    lambda x, a, b, c, *_: poly(x, [a, b, c], [2, 1, 0]) / (a / 3 + b / 2 + c),
    lambda x, a, *_: a * np.exp(a * x) / (np.exp(a) - 1),
]

lims = [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1)]


@test("Check if pdf return value return value between [0, 1] inside validity domaine")
def _(func=each(*functions), pdf=each(*prob_dens), lim=each(*lims)):
    x = np.linspace(0, 1, 1024)
    a = uniform(0, 1)
    b = uniform(0, 1)
    c = uniform(0, 1)
    y = pdf(x, a, b, c)
    f = pdf_normed(lambda x: func(x, a, b, c), lim)
    assert_allclose(y, f(x))
    assert_allclose(f(lim[0] - 1), 0, atol=1e-7)
    assert_allclose(f(lim[1] + 10), 0, atol=1e-7)
