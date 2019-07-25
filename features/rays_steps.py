from aloe import step, world
from Ray import Ray
from Tuple4 import Point, Vector

@step(r'([A-Za-z][A-Za-z0-9_]*) <- ray\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9_]*)\)')
def _ray_from_names(self, name1, name2, name3):
    setattr(world, name1, Ray(getattr(world, name2), getattr(world, name3)))


@step(r'([A-Za-z][A-Za-z0-9_]*) <- ray\(point\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\s*,\s*vector\('
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\)')
def _ray_from_values(self, name, px, py, pz, vx, vy, vz):
    setattr(world, name, Ray(Point(float(px), float(py), float(pz)),
                             Vector(float(vx), float(vy), float(vz))))


@step(r'([A-Za-z][A-Za-z0-9_]*)\.(origin|direction)\s*=\s*'
      r'([A-Za-z][A-Za-z0-9_]*)$')
def _ray_member_equals_name(self, name1, member, name2):
    print("\nExpected:")
    print(getattr(world, name2))
    print("\nGot:")
    print(getattr(getattr(world, name1), member))
    assert getattr(getattr(world, name1), member) == getattr(world, name2)


@step(r'position\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*([-+]?\d*\.?\d+)\)\s*=\s*'
      r'point\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\)')
def _position_equals_point(self, name, t, px, py, pz):
    test_point = Point(float(px), float(py), float(pz))
    print("\nExpected:")
    print(test_point)
    print("\nGot:")
    print(getattr(world, name).position(float(t)))
    assert getattr(world, name).position(float(t)) == test_point


@step(r'([A-Za-z][A-Za-z0-9_]*) <- transform\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _transform_ray(self, ray1, ray2, transform):
    setattr(world, ray1,
            getattr(world, ray2).transform(getattr(world, transform)))


@step(r'ray ([A-Za-z][A-Za-z0-9_]*)\.origin\s*=\s*point\(([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _ray_origin_equals_point(self, name, x, y, z):
    test_point = Point(float(x), float(y), float(z))
    print("\nExpected:")
    print(test_point)
    print("\nGot:")
    print(getattr(world, name).origin)
    assert getattr(world, name).origin == test_point


@step(r'ray ([A-Za-z][A-Za-z0-9_]*)\.direction\s*=\s*vector\(([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _ray_direction_equals_vector(self, name, x, y, z):
    test_vector = Vector(float(x), float(y), float(z))
    print("\nExpected:")
    print(test_vector)
    print("\nGot:")
    print(getattr(world, name).direction)
    assert getattr(world, name).direction == test_vector
