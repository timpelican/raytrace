from aloe import world, step
from Stripe import Stripe
from Tuple4 import Point, Colour
from Transformation import Scaling, Translation

@step(r'([A-Za-z][A-Za-z0-9_]*) <- stripe_pattern\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _stripe_pattern(self, name, c1, c2):
    col1 = getattr(world, c1)
    col2 = getattr(world, c2)
    p = Stripe(col1, col2)
    setattr(world, name, p)


@step(r'([A-Za-z][A-Za-z0-9_]*)\.(a|b)\s*=\s*colour ([A-Za-z][A-Za-z0-9_]*)')
def _check_pattern_colour(self, name, element, colour):
    p = getattr(world, name)
    c = getattr(world, colour)
    print("\nExpected:")
    print(c)
    print("\nGot:")
    print(getattr(p, element))
    assert getattr(p, element) == c


@step(r'stripe_at\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*point\(([-+]?\d*.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\)'
      r'\s*=\s*colour ([A-Za-z][A-Za-z0-9_]*)')
def _check_stripe_at(self, name, px, py, pz, colour):
    p = Point(float(px), float(py), float(pz))
    c = getattr(world, colour)
    pat = getattr(world, name)
    col = pat.stripe_at(p)
    print("\nExpected:")
    print(c)
    print("\nGot:")
    print(col)
    assert col == c


@step(r'([A-Za-z][A-Za-z0-9_]*)\.pattern <- stripe_pattern\(colour\('
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)'
      r'\s*,\s*colour\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\)\)')
def _set_material_stripe_pattern(self, name, r1, g1, b1, r2, g2, b2):
    m = getattr(world, name)
    c1 = Colour(float(r1), float(g1), float(b1))
    c2 = Colour(float(r2), float(g2), float(b2))
    m.pattern = Stripe(c1, c2)


@step(r'set_transform\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*scaling\(([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\)')
def _set_object_scaling(self, name, sx, sy, sz):
    t = Scaling(float(sx), float(sy), float(sz))
    getattr(world, name).transform = t


@step(r'([A-Za-z][A-Za-z0-9_]*) <- stripe_at_object\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'point\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\)\)')
def _get_stripe_at_object(self, colour, pattern, object, px, py, pz):
    pw = Point(float(px), float(py), float(pz))
    # Point is in world space, first transform to object space
    po = getattr(world, object).inverse_transform * pw
    # Pattern will handle the transform from object to pattern space
    c = getattr(world, pattern).stripe_at(po)
    setattr(world, colour, c)


@step(r'([A-Za-z][A-Za-z0-9_]*)\s*=\s*colour ([A-Za-z][A-Za-z0-9_]*)')
def _check_colour_by_name(self, c1, c2):
    colour = getattr(world, c1)
    test_colour = getattr(world, c2)
    print("\nExpected:")
    print(test_colour)
    print("\nGot:")
    print(colour)
    assert colour == test_colour


@step(r'set_pattern_transform\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*scaling\('
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\)')
def _set_pattern_scaling(self, name, sx, sy, sz):
    t = Scaling(float(sx), float(sy), float(sz))
    getattr(world, name).transform = t


@step(r'set_pattern_transform\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*translation\('
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\)')
def _set_pattern_scaling(self, name, tx, ty, tz):
    t = Translation(float(tx), float(ty), float(tz))
    getattr(world, name).transform = t
