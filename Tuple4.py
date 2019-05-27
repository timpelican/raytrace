# 4-item tuples as a maths building block for raytrace

from maths import equals    # American naming means we can call ours 'maths'
from math import sqrt
import Transformation


class Tuple4(object):
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
        if isinstance(m, float) or isinstance(m, int):
            return Tuple4(self.x * m, self.y * m, self.z * m, self.w * m)
        # Only valid for Colours, which is why we should have a subclass
        elif isinstance(m, Tuple4):
            return Colour(self.red * m.red,
                          self.green * m.green,
                          self.blue * m.blue)
        else:  # Throw an clearer exception?
            raise

    def __div__(self, d):
        return self.__truediv__(d)

    def __truediv__(self, d):
        return Tuple4(self.x / d, self.y / d, self.z / d, self.w / d)

    def __str__(self):
        # No f-strings pre 3.6
        return '{x}, {y}, {z}, {w}'.format(x=self.x, y=self.y, z=self.z,
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

    # Alias hacks for colour

    def get_red(self):
        return self.x

    def set_red(self, r):
        self.x = float(r)

    def get_green(self):
        return self.y

    def set_green(self, g):
        self.y = float(g)

    def get_blue(self):
        return self.z

    def set_blue(self, b):
        self.z = float(b)

    red = property(get_red, set_red)
    green = property(get_green, set_green)
    blue = property(get_blue, set_blue)

    def translate(self, x, y, z):
        m = Transformation.Translation(x, y, z)
        return m * self

    def scale(self, x, y, z):
        m = Transformation.Scaling(x, y, z)
        return m * self

    def rotate_x(self, rads):
        m = Transformation.Rotation_x(rads)
        return m * self

    def rotate_y(self, rads):
        m = Transformation.Rotation_z(rads)
        return m * self

    def rotate_z(self, rads):
        m = Transformation.Rotation_z(rads)
        return m * self

    def shear(self, xy, xz, yx, yz, zx, zy):
        m = Transformation.Shearing(xy, xz, yx, yz, zx, zy)
        return m * self

    def reflect(self, normal):
        return self - (normal * 2 * self.dot(normal))


def Point(x, y, z):
    # TODO: validation
    return Tuple4(x, y, z, 1.0)


def Vector(x, y, z):
    # TODO: validation
    return Tuple4(x, y, z, 0)

# TODO: This should really be a subclass, the behaviour is different
# TODO: and so are the attributes.
# TODO: Hack as aliases for the moment.


def Colour(r, g, b):
    return Tuple4(r, g, b, 0)
