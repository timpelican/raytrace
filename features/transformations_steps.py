from __future__ import print_function
from aloe import step, world
from Transformation import Translation, Scaling, Rotation_x, Rotation_y,\
    Rotation_z, Shearing, ViewTransform
from Tuple4 import Point, Vector


@step(r'([A-Za-z][A-Za-z0-9_]*) <- translation\s*\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def __translation(self, name, x, y, z):
    setattr(world, name, Translation(float(x), float(y), float(z)))


@step(r'([A-Za-z][A-Za-z0-9_]*)\s*\*\s*([A-Za-z][A-Za-z0-9_]*)'
      r'\s*=\s*point\s*\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\)')
def __mupltiply_matrix_point(self, name1, name2, x, y, z):
    test_point = Point(float(x), float(y), float(z))
    print("\nTransformation matrix is:")
    print(getattr(world, name1))
    print("\nExpected:")
    print(test_point)
    print("\nGot:")
    print(getattr(world, name1) * getattr(world, name2))
    assert getattr(world, name1) * getattr(world, name2) == test_point


@step(r'([A-Za-z][A-Za-z0-9_]*)\s*\*\s*([A-Za-z][A-Za-z0-9_]*)'
      r'\s*=\s*vector\s*([A-Za-z][A-Za-z0-9_]*)')
def __mupltiply_matrix_vector_by_name(self, name1, name2, name3):
    print("\nExpected:")
    print(getattr(world, name3))
    print("\nGot:")
    print(getattr(world, name1) * getattr(world, name2))
    assert getattr(world, name1) * getattr(world, name2) == \
        getattr(world, name3)


@step(r'([A-Za-z][A-Za-z0-9_]*)\s*\*\s*([A-Za-z][A-Za-z0-9_]*)'
      r'\s*=\s*vector\s*\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\)')
def __mupltiply_matrix_vector(self, name1, name2, x, y, z):
    test_vector = Vector(float(x), float(y), float(z))
    print("\nExpected:")
    print(test_vector)
    print("\nGot:")
    print(getattr(world, name1) * getattr(world, name2))
    assert getattr(world, name1) * getattr(world, name2) == test_vector


@step(r'([A-Za-z][A-Za-z0-9_]*) <- scaling\s*\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def __scaling(self, name, x, y, z):
    setattr(world, name, Scaling(float(x), float(y), float(z)))


@step(r'([A-Za-z][A-Za-z0-9_]*) <- rotation_x\s*\(([-+]?\d*\.?\d+)\)')
def __rotation_x(self, name, rads):
    setattr(world, name, Rotation_x(float(rads)))


@step(r'([A-Za-z][A-Za-z0-9_]*) <- rotation_y\s*\(([-+]?\d*\.?\d+)\)')
def __rotation_y(self, name, rads):
    setattr(world, name, Rotation_y(float(rads)))


@step(r'([A-Za-z][A-Za-z0-9_]*) <- rotation_z\s*\(([-+]?\d*\.?\d+)\)')
def __rotation_z(self, name, rads):
    setattr(world, name, Rotation_z(float(rads)))


@step(r'([A-Za-z][A-Za-z0-9_]*) <- shearing\s*\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def __shearing(self, name, xy, xz, yx, yz, zx, zy):
    setattr(world, name, Shearing(float(xy), float(xz), float(yx), float(yz),
                                  float(zx), float(zy)))


@step(r'([A-Za-z][A-Za-z0-9_]*) <- ([A-Za-z][A-Za-z0-9_]*).translate\('
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _translate_method(self, name1, name2, x, y, z):
    setattr(world, name1, getattr(world, name2).translate(float(x), float(y),
                                                          float(z)))


@step(r'([A-Za-z][A-Za-z0-9_]*) <- ([A-Za-z][A-Za-z0-9_]*).rotate_x\('
      r'([-+]?\d*\.?\d+)\).scale\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\).translate\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _method_chain(self, name1, name2, rads, sx, sy, sz, tx, ty, tz):
    setattr(world, name1, getattr(world, name2).rotate_x(float(rads)).
            scale(float(sx), float(sy), float(sz)).
            translate(float(tx), float(ty), float(tz)))


@step(r'([A-Za-z][A-Za-z0-9_]*) <- view_transform\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _view_transformation_by_name(self, name1, name2, name3, name4):
    p_from = getattr(world, name2)
    p_to = getattr(world, name3)
    v_up = getattr(world, name4)
    setattr(world, name1, ViewTransform(p_from, p_to, v_up))


@step(r'([A-Za-z][A-Za-z0-9_]*) = scaling\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _check_scaling_by_value(self, name, x, y, z):
    test_matrix = Scaling(float(x), float(y), float(z))
    print("\nExpected:")
    print(test_matrix)
    print("\nGot:")
    print(getattr(world, name))
    assert getattr(world, name) == test_matrix


@step(r'([A-Za-z][A-Za-z0-9_]*) = translation\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _check_translation_by_value(self, name, x, y, z):
    test_matrix = Translation(float(x), float(y), float(z))
    print("\nExpected:")
    print(test_matrix)
    print("\nGot:")
    print(getattr(world, name))
    assert getattr(world, name) == test_matrix
