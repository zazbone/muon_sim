from ward import test, skip
from random import uniform
from utils import cst, pdf_normal
from muon_sim.sampler import MCMCSampler
import numpy as np
from numpy.testing import assert_allclose


# @skip("not implemented yet")
# TODO: Make the tests not crash randomly (lol)
# TODO: Find other test variables for distribs
@test("1 dimension mcmc sampler, test based on pdf parameters check")
def _():
    NW = 2**10
    NC = 2**10
    # Uniform distribution
    mean = uniform(-10, 10)
    L = uniform(0, 10)
    tol = L * 1e-2
    uniform_sampler = MCMCSampler(lambda x: cst(x, 4), (mean - L, mean + L), NW)
    y = uniform_sampler.sample(NC).flatten()
    assert_allclose(np.mean(y), mean, rtol=tol, atol=tol)
    assert_allclose(np.var(y), 1 / 3 * L**2, rtol=tol, atol=tol)
    h, bedges = np.histogram(y, bins=256, density=True)
    bins = 0.5 * (bedges[1:] + bedges[0:-1])
    assert_allclose(h, 1 / (2 * L), rtol=tol, atol=tol)

    # Normal distribution
    # var = L
    # normal_sampler = MCMCSampler(
    #     lambda x: pdf_normal(x, mean, var), (mean - 10 * L, mean + 10 * L), NW
    # )
    # y = normal_sampler.sample(NC).flatten()
    # assert_allclose(np.mean(y), mean, rtol=tol, atol=tol)
    # assert_allclose(np.var(y), var, rtol=tol, atol=tol)
    # h, bedges = np.histogram(y, bins=256, density=True)
    # bins = 0.5 * (bedges[1:] + bedges[0:-1])
    # assert_allclose(h, pdf_normal(h, mean, var, True), rtol=tol, atol=tol)

    # TODO:
    # exponential distribution
    # gamma distribution
    # beta distribution
    # student's t-distribution
    # Cauchy distribution
    # Cauchy distribution
