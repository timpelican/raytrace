# 4-item tuples as a maths building block for raytrace

from maths import equals    # American naming means we can call ours 'maths'
from math import sqrt


class Tuple4:
    def __init__(self, x, y, z, w):
        # TODO: Any kind of validation
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other):
        if (equals(self.x, other.x) and equals(self.y, other.y)
                and equals(self.z, other.z) and equals(self.z, other.z)):
            return True
        else:
            return False

    def __add__(self, other):
        return Tuple4(self.x + other.x, self.y + other.y,
                      self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return Tuple4(self.x - other.x, self.y - other.y,
                      self.z - other.z, self.w - other.w)

    def __neg__(self):
        return Tuple4(-self.x, -self.y, -self.z, -self.w)

    def __mul__(self, m):
        return Tuple4(self.x * m, self.y * m, self.z * m, self.w * m)

    def __div__(self, d):
        return Tuple4(self.x / d, self.y / d, self.z / d, self.w / d)

    def __str__(self):
        # No f-strings pre 3.6
        return '{x}, {y}, {z}. {w}'.format(x=self.x, y=self.y, z=self.z,
                                           w=self.w)

    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2)

    def normalize(self):
        mag = self.magnitude()
        return Tuple4(self.x / mag, self.y / mag, self.z / mag,
                      self.w / mag)

    def dot(self, other):
        return self.x * other.x + \
               self.y * other.y + \
               self.z * other.z + \
               self.w * other.w

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)


def Point(x, y, z):
    # TODO: validation
    return Tuple4(x, y, z, 1.0)


def Vector(x, y, z):
    # TODO: validation
    return Tuple4(x, y, z, 0)
