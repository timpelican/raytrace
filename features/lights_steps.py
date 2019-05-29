from aloe import world, step
from Light import PointLight


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
