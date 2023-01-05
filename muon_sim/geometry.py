class Ray:
    def __init__(self, x0, y0, z0, dx, dy, dz):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.dx = dx
        self.dy = dy
        self.dz = dz

class Disc:
    def __init__(self, radius, x0=0, y0=0, z0=0):
        pass

    def ray_intersec(self, ray):
        pass

class Cylinder:
    def __init__(self, radius, height, x0=0, y0=0, z0=0):
        pass

    def ray_intersec(self, ray):
        pass