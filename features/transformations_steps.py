from __future__ import print_function
from aloe import step, world
from Transformation import Translation
from Tuple4 import Point


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
