from aloe import world, step
from Material import Material
from Tuple4 import Colour


@step(r'([A-Za-z][A-Za-z0-9]*) <- material\(\)')
def _default_material(self, name):
    setattr(world, name, Material())


@step(r'([A-Za-z][A-Za-z0-9_]*)\.colour\s*=\s*colour\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _check_colour_value(self, name, r, g, b):
    test_colour = Colour(float(r), float(g), float(b))
    print("\nExpected:")
    print(test_colour)
    print("\nGot:")
    print(getattr(world, name).colour)
    assert getattr(world, name).colour == test_colour


@step(r'([A-Za-z][A-Za-z0-9_]*)\.(ambient|diffuse|specular|shininess)\s*=\s*'
      r'([-+]?\d*\.?\d+)')
def _material_member_equals_value(self, name, member, value):
    test_value = float(value)
    print("\nExpected:")
    print(value)
    print("\nGot:")
    print(getattr(getattr(world, name), member))
    assert getattr(getattr(world, name), member) == test_value
