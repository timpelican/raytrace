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


@step(r'When ([A-Za-z][A-Za-z0-9_]*) <- lighting\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9_]*)\)')
def _check_lighting(self, name, mat, light, pos, eye, norm, shadow):
    setattr(world, name,
            getattr(world, mat).lighting(getattr(world, light),
                                         getattr(world, pos),
                                         getattr(world, eye),
                                         getattr(world, norm),
                                         getattr(world, shadow)))


@step(r'colour ([A-Za-z][A-Za-z0-9_]*)\s*=\s*colour\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _check_named_colour_value(self, name, r, g, b):
    test_colour = Colour(float(r), float(g), float(b))
    print("\nExpected:")
    print(test_colour)
    print("\nGot:")
    print(getattr(world, name))
    assert getattr(world, name) == test_colour


@step(r'([A-Za-z][A-Za-z0-9_]*) <- (true|false)')
def _set_true_false(self, name, value):
    if value == "true":
        setattr(world, name, True)
    else:
        setattr(world, name, False)
