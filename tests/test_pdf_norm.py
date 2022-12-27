from ward import test
from utils import cst, linear, poly
from muon_sim.mcmc import pdf_normed
import numpy as np
from numpy.testing import assert_allclose
from numpy.random import uniform


@test("Check if pdf return value return value between [0, 1] inside validity domaine")
def _():
    # f(x) -> f(x) / (F(1) - F(0)) if x in [0, 1] else 0
    x = np.linspace(0, 1, 1024)

    # sin(x) -> sin(x) / (1 - cos(1))
    y = np.sin(x) / (1 - np.cos(1))
    f = pdf_normed(np.sin, (0, 1))
    assert_allclose(y, f(x))
    assert_allclose(f(-1), 0, atol=1e-7)
    assert_allclose(f(10), 0, atol=1e-7)

    # cst=4 -> cst=1
    a = uniform(0, 1)
    y = cst(x, 1)
    f = pdf_normed(lambda x: cst(x, a), (0, 1))
    assert_allclose(y, f(x))
    assert_allclose(f(-1), 0, atol=1e-7)
    assert_allclose(f(10), 0, atol=1e-7)

    # a * x + b -> (a * x + b) / (0.5 * a + b)
    b = uniform(0, 1)
    y = linear(x, a, b) / (0.5 * a + b)
    f = pdf_normed(lambda x: linear(x, a, b), (0, 1))
    assert_allclose(y, f(x))
    assert_allclose(f(-1), 0, atol=1e-7)
    assert_allclose(f(10), 0, atol=1e-7)

    # a * x^2 + b * x + c -> a * x^2 + b * x + c / (a/3 + b/2 + c)
    c = uniform(0, 1)
    y = poly(x, [a, b, c], [2, 1, 0]) / (a / 3 + b / 2 + c)
    f = pdf_normed(lambda x: poly(x, [a, b, c], [2, 1, 0]), (0, 1))
    assert_allclose(y, f(x))
    assert_allclose(f(-1), 0, atol=1e-7)
    assert_allclose(f(10), 0, atol=1e-7)

    # exp(a * x) -> a * exp(a * x) / (exp(a) - 1)
    y = a * np.exp(a * x) / (np.exp(a) - 1)
    f = pdf_normed(lambda x: np.exp(a * x), (0, 1))
    assert_allclose(y, f(x))
    assert_allclose(f(-1), 0, atol=1e-7)
    assert_allclose(f(10), 0, atol=1e-7)
