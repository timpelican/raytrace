from aloe import step, world
from tuple4 import tuple4

# TODO: This should only accept numbers


@step(r'(\S+) is a tuple\s*\((\S+),\s*(\S+),\s*(\S+),\s*(\S+)\)')
def _a_is_a_tuple(self, name, x, y, z, w):
    setattr(world, name, tuple4(x, y, z, w))


# TODO: This is probably going to match way more than I need to.
# TODO: Plan to write something more specific once I add more classes.


@step(r'(\S+)\.(\S+)\s*=\s*(\S+)')
def _tuple_equals(self, name, member, value):
    if getattr(getattr(world, name), member) == value:
        return True
    else:
        return False


@step(r'(\S+) is a point')
def _is_a_point(self, name):
    if getattr(world, name).w == 1.0:
        return True
    else:
        return False


@step(r'(\S+) is not a point')
def _is_not_a_point(self, name):
    if getattr(world, name).w == 1.0:
        return False
    else:
        return True


@step(r'(\S+) is a vector')
def _is_a_vector(self, name):
    if getattr(world, name).w == 0.0:
        return True
    else:
        return False


@step(r'(\S+) is not a vector')
def _is_not_a_vector(self, name):
    if getattr(world, name).w == 0.0:
        return False
    else:
        return True
