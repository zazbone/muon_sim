from ward import test, skip
import numpy as np
from numpy.random import random, uniform
from numpy.testing import assert_allclose
from muon_sim.geometry import Disc, Vector, Ray, Cylinder
from muon_sim.mcmc import random_circle


@test("Vector transformations")
def _():
    N = 10
    vec = Vector(random(N), random(N), random(N))
    a = Vector(random(N), random(N), random(N))
    theta = uniform(0, 2 * np.pi, N)
    phi = uniform(0 + 0.1, np.pi - 0.1, N)
    vecp = vec.roty(phi).rotz(theta).translate(a)
    vecp = vecp.translate(-a).rotz(-theta).roty(-phi)
    assert np.all(vecp.isclose(vec))

@skip()
@test("test intersection with disc")
def _():
    N = 10
    disc = Disc(1)
    a = Vector(0.2, 0.8, -0.5)
    theta = -0.3
    phi = 1.2
    disc.origin = disc.origin.translate(a)
    disc.normal = disc.normal.roty(phi).rotz(theta)

    r0 = Vector(*random_circle(N, 0.8), 0.1).translate(a)
    d = Vector(np.zeros(N), np.zeros(N), -np.ones(N)).roty(phi).rotz(theta)
    raygood = Ray(r0, d)

    lmb = disc.ray_intersec(raygood)
    # Non invalid values
    assert not np.any(lmb.mask)


@test("test intersection with cylinder")
def _():
    N = 10
    cyl = Cylinder(0.4, 0.6, Vector(0, 0, 0), Vector(0, 0, 1))
    r0 = Vector(*random_circle(N, 20), np.zeros(N))
    d = -r0  # Should all converge throug the cylinder
    raygood = Ray(r0, d)

    *_, valid = cyl.ray_intersec(raygood)
    assert np.all(valid)

    r0 = Vector(r0.x, r0.y, r0.z + 10)
    raybad = Ray(r0, d)
    *_, valid = cyl.ray_intersec(raybad)
    assert not np.any(valid)


@skip("not implemented yet")
@test("test full geometry")
def _():
    pass
