from aloe import step, world
from tuple4 import tuple4
from maths import equals


@step(r'(\S+) is a tuple\s*\(([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+),'
    r'\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)\)')
def _a_is_a_tuple(self, name, x, y, z, w):
    setattr(world, name, tuple4(float(x), float(y), float(z), float(w)))


# Matches only members x, y, z, w and floats, which should be enough
# to restrict it to tuples.


@step(r'(\S+)\.([xyzw])\s*=\s*([-+]?\d*\.?\d+)')
def _tuple_equals(self, name, member, value):
    if equals(getattr(getattr(world, name), member), float(value)):
        return True
    else:
        return False


@step(r'(\S+) is a point')
def _is_a_point(self, name):
    if equals(getattr(world, name).w, 1.0):
        return True
    else:
        return False


@step(r'(\S+) is not a point')
def _is_not_a_point(self, name):
    if equals(getattr(world, name).w, 1.0):
        return False
    else:
        return True


@step(r'(\S+) is a vector')
def _is_a_vector(self, name):
    if equals(getattr(world, name).w, 0.0):
        return True
    else:
        return False


@step(r'(\S+) is not a vector')
def _is_not_a_vector(self, name):
    if equals(getattr(world, name).w, 0.0):
        return False
    else:
        return True
