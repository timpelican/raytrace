from __future__ import print_function
from aloe import step, world
from Transformation import Translation, Scaling
from Tuple4 import Point, Vector


@step(r'([A-Za-z][A-Za-z0-9]*) <- translation\s*\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def __translation(self, name, x, y, z):
    setattr(world, name, Translation(float(x), float(y), float(z)))


@step(r'([A-Za-z][A-Za-z0-9]*)\s*\*\s*([A-Za-z][A-Za-z0-9]*)'
      r'\s*=\s*point\s*\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\)')
def __mupltiply_matrix_point(self, name1, name2, x, y, z):
    test_point = Point(float(x), float(y), float(z))
    print("\nExpected:")
    print(test_point)
    print("\nGot:")
    print(getattr(world, name1) * getattr(world, name2))
    assert getattr(world, name1) * getattr(world, name2) == test_point


@step(r'([A-Za-z][A-Za-z0-9]*)\s*\*\s*([A-Za-z][A-Za-z0-9]*)'
      r'\s*=\s*vector\s*([A-Za-z][A-Za-z0-9]*)')
def __mupltiply_matrix_vector_by_name(self, name1, name2, name3):
    print("\nExpected:")
    print(getattr(world, name3))
    print("\nGot:")
    print(getattr(world, name1) * getattr(world, name2))
    assert getattr(world, name1) * getattr(world, name2) == \
        getattr(world, name3)


@step(r'([A-Za-z][A-Za-z0-9]*)\s*\*\s*([A-Za-z][A-Za-z0-9]*)'
      r'\s*=\s*vector\s*\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\)')
def __mupltiply_matrix_vector(self, name1, name2, x, y, z):
    test_vector = Vector(float(x), float(y), float(z))
    print("\nExpected:")
    print(test_vector)
    print("\nGot:")
    print(getattr(world, name1) * getattr(world, name2))
    assert getattr(world, name1) * getattr(world, name2) == test_vector


@step(r'([A-Za-z][A-Za-z0-9]*) <- scaling\s*\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def __scaling(self, name, x, y, z):
    setattr(world, name, Scaling(float(x), float(y), float(z)))
