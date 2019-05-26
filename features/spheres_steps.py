from aloe import world, step
from Sphere import Sphere
from Matrix import IdentityMatrix
from maths import equals
from Tuple4 import Point


@step(r'([A-Za-z][A-Za-z0-9_]*) <- sphere\(\)')
def _sphere(self, name):
    setattr(world, name, Sphere())


@step(r'([A-Za-z][A-Za-z0-9_]*) <- intersect\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _intersects(self, name1, name2, name3):
    setattr(world, name1,
            getattr(world, name2).intersects(getattr(world, name3)))


@step(r'([A-Za-z][A-Za-z0-9_]*).count\s*=\s*(\d+)')
def _count_equals_value(self, name, value):
    print("\nExpected:")
    print(int(value))
    print("\nGot:")
    print(len(getattr(world, name)))
    assert len(getattr(world, name)) == int(value)


@step(r'([A-Za-z][A-Za-z0-9_]*)\[(\d+)\]\s*=\s*([-+]?\d*\.?\d+)')
def _index_equals_value(self, name, index, value):
    print("\nExpected:")
    print(float(value))
    print("\nGot:")
    print(getattr(world, name)[int(index)])
    assert equals(getattr(world, name)[int(index)], float(value))


@step(r'([A-Za-z][A-Za-z0-9_]*)\.transform is the identity_matrix')
def _check_transform_identity(self, name):
    test_matrix = IdentityMatrix(4)
    print("\nExpected:")
    print(test_matrix)
    print("\nGot:")
    print(getattr(world, name).transform)
    assert getattr(world, name).transform == test_matrix


@step(r'set_transform\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9_]*)\)')
def _set_transform(self, obj, transform):
    getattr(world, obj).transform = getattr(world, transform)


@step(r'([A-Za-z][A-Za-z0-9_]*)\.transform\s*=\s*([A-Za-z][A-Za-z0-9_]*)')
def _check_transform_name(self, name1, name2):
    test_matrix = getattr(world, name2)
    print("\nExpected:")
    print(test_matrix)
    print("\nGot:")
    print(getattr(world, name1).transform)
    assert getattr(world, name1).transform == test_matrix


@step(r'([A-Za-z][A-Za-z0-9_]*) <- normal_at\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'point\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\)\)')
def _normal_at_point(self, name1, name2, x, y, z):
    p = Point(float(x), float(y), float(z))
    n = getattr(world, name2).normal_at(p)
    setattr(world, name1, n)
