from aloe import step, world
from Shape import Shape, TestShape
from Tuple4 import Point, Vector


@step(r'([A-Za-z][A-Za-z0-9_]*) <- test_shape\(\)$')
def _sphere(self, name):
    setattr(world, name, TestShape())


@step(r'([A-Za-z][A-Za-z0-9_]*)\.saved_ray\.origin\s*=\s*point\('
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _check_saved_ray_origin(self, name, px, py, pz):
    test_point = Point(float(px), float(py), float(pz))
    point = getattr(world, name).saved_ray.origin
    print("\nExpected:")
    print(test_point)
    print("\nGot:")
    print(point)
    assert point == test_point


@step(r'([A-Za-z][A-Za-z0-9_]*)\.saved_ray\.direction\s*=\s*vector\('
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _check_saved_ray_direction(self, name, vx, vy, vz):
    test_vector = Vector(float(vx), float(vy), float(vz))
    vector = getattr(world, name).saved_ray.direction
    print("\nExpected:")
    print(test_vector)
    print("\nGot:")
    print(vector)
    assert vector == test_vector


@step(r'([A-Za-z][A-Za-z0-9_]*) is a shape')
def _is_a_shape(self, name):
    test_shape = getattr(world, name)
    assert isinstance(test_shape, Shape)
