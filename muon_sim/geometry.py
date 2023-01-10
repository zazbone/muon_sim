"""
Worst geometry lib possible, should use dataclass
"""


import numpy as np


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
    
    def __div__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar) 

    @classmethod
    def zero(cls):
        return cls(0, 0, 0)

    def euler_angle(self):
        r = np.sqrt(np.power(self.x, 2) + np.power(self.y, 2) + np.power(self.z, 2))
        dx = self.x / r
        dz = self.z / r
        phi = np.arccos(dz)
        theta = np.zeros(phi.shape)
        # Necessary instead of where else raise runtime error
        mask = np.logical_not(np.isclose(np.sin(phi), 0))
        theta[mask] = np.arccos(dx[mask] / np.sin(phi[mask]))
        return theta, phi
    
    def norm(self):
        return np.sqrt(np.power(self.x, 2), np.power(self.y, 2), np.power(self.z, 2))

    def translate(self, a):
        return Vector(self.x + a.x, self.y + a.y, self.z + a.z)

    def roty(self, phi):
        cs = np.cos(phi)
        ss = np.sin(phi)
        return Vector(self.x * cs + self.z * ss, self.y, -self.x * ss + self.z * cs)

    def rotz(self, theta):
        cs = np.cos(theta)
        ss = np.sin(theta)
        return Vector(self.x * cs - self.y * ss, self.x * ss + self.y * cs, self.z)

    def isclose(self, other):
        tx = np.isclose(self.x, other.x)
        ty = np.logical_and(tx, np.isclose(self.y, other.y))
        return np.logical_and(ty, np.isclose(self.z, other.z))


class Ray:
    def __init__(self, origin: Vector, direction: Vector):
        self.r0 = origin
        self.dir = direction

    def translate(self, a: Vector):
        return Ray(self.r0.translate(a), self.dir)

    def roty(self, phi):
        return Ray(self.r0, self.dir.roty(phi))

    def rotz(self, theta):
        return Ray(self.r0, self.dir.rotz(theta))

    def get_pos(self, lamb):
        return Vector(
            self.r0.x + lamb * self.dir.x,
            self.r0.y + lamb * self.dir.y,
            self.r0.z + lamb * self.dir.z,
        )


class Disc:
    def __init__(self, radius, origin=None, normal=None):
        self.radius = radius
        if normal is None:
            normal = Vector(0, 0, 1)
        self.normal = normal
        if origin is None:
            origin = Vector.zero()
        self.origin = origin

    def ray_intersec(self, ray: Ray):
        theta, phi = self.normal.euler_angle()
        ray = ray.translate(-self.origin).rotz(-theta).roty(-phi)
        invalid = np.isclose(ray.dir.z, 0)
        lamb = np.where(invalid, 0, -ray.r0.z / ray.dir.z)
        intersec = ray.get_pos(lamb)
        r = np.sqrt(np.power(intersec.x, 2) + np.power(intersec.y, 2))
        print(intersec.z)
        print(r)
        invalid = np.logical_or(invalid, r > self.radius)
        return lamb, invalid


class Cylinder:
    def __init__(
        self, radius, height, origin: Vector = None, orientation: Vector = None
    ):
        self.radius = radius
        self.height = height
        if orientation is None:
            orientation = Vector(0, 0, 1)
        self.orientation = orientation
        if origin is None:
            origin = Vector.zero()
        self.origin = origin

    def ray_intersec(self, ray: Ray):
        # Change Ray frame to frame where self.orientation // \vec{z}
        theta, phi = self.orientation.euler_angle()
        ray = ray.translate(-self.origin).rotz(-theta).roty(-phi)
        # Check for divergent solution
        r = np.sqrt(np.power(ray.r0.x, 2) + np.power(ray.r0.y, 2))
        check_div = np.logical_or(self.radius != r, ray.dir.z != 0)
        # Polynomial solution parameters
        a = np.power(ray.dir.x, 2) + np.power(ray.dir.y, 2)
        b = 2 * (ray.r0.x * ray.dir.x + ray.r0.y * ray.dir.y)
        c = r - self.radius
        delta = np.power(b, 2) - 4 * a * c
        # Separate different Delta case and associated solutions
        check_delta = np.logical_and(delta >= 0, check_div)
        is_lbd0_sol = np.isclose(delta, 0) & check_delta
        n0delta = np.logical_not(np.isclose(delta, 0))
        is_lbdp_sol = check_delta & n0delta
        is_lbdm_sol = check_delta & n0delta
        lambda0 = np.where(is_lbd0_sol, -b / (2 * a), 0)
        lambdap = np.where(is_lbdp_sol, (-b + np.sqrt(delta)) / (2 * a), 0)
        lambdam = np.where(is_lbdm_sol, (-b - np.sqrt(delta)) / (2 * a), 0)
        # Check z boundary of solutions
        h = self.height / 2
        z0 = ray.get_pos(lambda0).z
        is_lbd0_sol = is_lbd0_sol & np.logical_and(-h <= z0, z0 <= h)
        lambda0 = np.where(is_lbd0_sol, lambda0, 0)  # Not necessary to set to 0 there
        zp = ray.get_pos(lambdap).z
        is_lbdp_sol = is_lbdp_sol & np.logical_and(-h <= zp, zp <= h)
        lambdap = np.where(is_lbdp_sol, lambdap, 0)
        zm = ray.get_pos(lambdam).z
        is_lbdm_sol = is_lbdm_sol & np.logical_and(-h <= zm, zm <= h)
        lambdam = np.where(is_lbdm_sol, lambdam, 0)
        # Pack the return values
        valid = is_lbd0_sol | is_lbdp_sol | is_lbdm_sol
        lmb = (lambda0, lambdap, lambdam)
        is_sol = (is_lbd0_sol, is_lbdp_sol, is_lbdm_sol)
        return lmb, is_sol, valid


class FullGeometry:
    def __init__(self, origin: Vector, height, radius, orientation: Vector):
        self.cylin = Cylinder(radius, height, origin, orientation)
        h = height / 2 * orientation / orientation.norm()
        self.top_disc = Disc(radius, origin.translate(h), orientation)
        self.bot_disc = Disc(radius, origin.translate(-h), orientation)