from aloe import step, world
from tuple4 import tuple4, point, vector
from maths import equals
from math import sqrt


@step(r'(\S+) <- tuple\s*\(([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)\)')
def _a_is_a_tuple(self, name, x, y, z, w):
    setattr(world, name, tuple4(float(x), float(y), float(z), float(w)))


# Matches only members x, y, z, w and floats, which should be enough
# to restrict it to tuples.


@step(r'(\S+)\.([xyzw])\s*=\s*([-+]?\d*\.?\d+)')
def _tuple_member_equals(self, name, member, value):
    assert equals(getattr(getattr(world, name), member), float(value))


@step(r'(-?)([A-Za-z0-9]+)\s*=\s*tuple\(([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)\)')
def _tuple_equals(self, negate, name, x, y, z, w):
    test_tuple = tuple4(float(x), float(y), float(z), float(w))
    if negate == "-":
        assert -getattr(world, name) == test_tuple
    else:
        assert getattr(world, name) == test_tuple


@step(r'([A-Za-z0-9]+)\s*\+\s*([A-Za-z0-9]+)\s*=\s*tuple\(([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)\)')
def _tuple_addition(self, name1, name2, x, y, z, w):
    test_tuple = tuple4(float(x), float(y), float(z), float(w))
    assert getattr(world, name1) + getattr(world, name2) == test_tuple


@step(r'([A-Za-z0-9]+)\s*\*\s*([-+]?\d*\.?\d+)\s*=\s*tuple\(([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)\)')
def _tuple_multiplication(self, name, multiplier, x, y, z, w):
    test_tuple = tuple4(float(x), float(y), float(z), float(w))
    assert getattr(world, name) * float(multiplier) == test_tuple


@step(r'([A-Za-z0-9]+)\s*/\s*([-+]?\d*\.?\d+)\s*=\s*tuple\(([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)\)')
def _tuple_division(self, name, divisor, x, y, z, w):
    test_tuple = tuple4(float(x), float(y), float(z), float(w))
    assert getattr(world, name) / float(divisor) == test_tuple


@step(r'([A-Za-z0-9]+)\s*\-\s*([A-Za-z0-9]+)\s*=\s*vector\(([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)')
def _vector_subtraction(self, name1, name2, x, y, z):
    test_tuple = vector(float(x), float(y), float(z))
    assert getattr(world, name1) - getattr(world, name2) == test_tuple


@step(r'([A-Za-z0-9]+)\s*\-\s*([A-Za-z0-9]+)\s*=\s*point\(([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)')
def _point_subtraction(self, name1, name2, x, y, z):
    test_tuple = point(float(x), float(y), float(z))
    assert getattr(world, name1) - getattr(world, name2) == test_tuple


@step(r'(\S+) <- point\s*\(([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+)\)')
def _p_is_a_point(self, name, x, y, z):
    setattr(world, name, point(float(x), float(y), float(z)))


@step(r'(\S+) <- vector\s*\(([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+)\)')
def _p_is_a_vector(self, name, x, y, z):
    setattr(world, name, vector(float(x), float(y), float(z)))


@step(r'(\S+) is a point')
def _is_a_point(self, name):
    assert equals(getattr(world, name).w, 1.0)


@step(r'(\S+) is not a point')
def _is_not_a_point(self, name):
    assert equals(getattr(world, name).w, 0.0)


@step(r'(\S+) is a vector')
def _is_a_vector(self, name):
    assert equals(getattr(world, name).w, 0.0)


@step(r'(\S+) is not a vector')
def _is_not_a_vector(self, name):
    assert equals(getattr(world, name).w, 1.0)


@step(r'magnitude\(([A-Za-z0-9]+)\)\s*=\s*([-+]?\d*\.?\d+)')
def _magnitude_vector(self, name, magnitude):
    assert equals(getattr(world, name).magnitude(), float(magnitude))


@step(r'magnitude\(([A-Za-z0-9]+)\)\s*=\s*sqrt\(([-+]?\d*\.?\d+)\)')
def _magnitude_vector_sqrt(self, name, magnitude):
    assert equals(getattr(world, name).magnitude(), sqrt(float(magnitude)))
