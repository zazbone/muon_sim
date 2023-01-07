import numpy as np


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    @classmethod
    def zero(cls):
        return cls(0, 0, 0)

    def euler_angle(self):
        r = np.sqrt(np.power(self.x, 2) + np.power(self.y, 2) + np.power(self.z, 2))
        dx = self.x / r
        dz = self.z / r
        phi = np.arccos(dz)
        theta = np.where(np.sin(phi) == 0, np.arccos(dx / np.sin(phi)), 0)
        return theta, phi

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
        theta, phi = self.orientation.euler_angle()
        ray = ray.translate(-self.origin).rotz(-theta).roty(-phi)
        r = np.sqrt(np.power(ray.r0.x, 2) + np.power(ray.r0.y, 2))
        invalid = np.logical_and(np.isclose(r, self.radius), np.isclose(ray.dir.z, 0))
        a = np.power(ray.dir.x, 2) + np.power(ray.dir.y, 2)
        b = 2 * (ray.r0.x * ray.dir.x + ray.r0.y * ray.dir.y)
        c = r - self.radius
        delta = np.power(b, 2) - 4 * a * c
        invalid = np.logical_or(invalid, delta < 0)
        nhit = invalid * (2 - np.isclose(delta, 0))
        lambda0 = np.where(nhit == 1, -b / (2 * a), 0)
        lambdap = np.where(nhit == 2, (-b + np.sqrt(delta)) / (2 * a), 0)
        lambdam = np.where(nhit == 2, (-b - np.sqrt(delta)) / (2 * a), 0)
        return nhit, lambda0, lambdap, lambdam, invalid
