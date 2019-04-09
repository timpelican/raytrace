# 4-item tuples as a maths building block for raytrace

from maths import equals


class tuple4:
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


def point(x, y, z):
    # TODO: validation
    return tuple4(x, y, z, 1.0)


def vector(x, y, z):
    # TODO: validation
    return tuple4(x, y, z, 0)
