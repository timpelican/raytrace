from aloe import world, step
from Light import PointLight
from Tuple4 import Point, Colour


@step(r'([A-Za-z][A-Za-z0-9]*) <- point_light\(([A-Za-z][A-Za-z0-9]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9]*)\)')
def _point_light_by_name(self, name, position, intensity):
    setattr(world, name,
            PointLight(getattr(world, position), getattr(world, intensity)))


@step(r'([A-Za-z][A-Za-z0-9_]*)\.(position|intensity)\s*=\s*'
      r'([A-Za-z][A-Za-z0-9_]*)$')
def _light_member_equals_name(self, name1, member, name2):
    print("\nExpected:")
    print(getattr(world, name2))
    print("\nGot:")
    print(getattr(getattr(world, name1), member))
    assert getattr(getattr(world, name1), member) == getattr(world, name2)


@step(r'([A-Za-z][A-Za-z0-9]*) <- point_light\(point\(([-+]?\d*\.?\d+)\s*,'
      r'\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\s*,\s*colour\('
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\)')
def _point_light_by_number(self, name, x, y, z, r, g, b):
    setattr(world, name,
            PointLight(Point(float(x), float(y), float(z)),
                       Colour(float(r), float(g), float(b))))
