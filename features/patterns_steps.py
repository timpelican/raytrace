from aloe import world, step
from Stripe import Stripe
from Tuple4 import Point, Colour
from Transformation import Scaling, Translation
from Pattern import TestPattern
from SolidColour import SolidColour
from Gradient import Gradient, BiGradient, RingGradient
from RingPattern import RingPattern
from Checkers import Checkers


@step(r'[^a-z0-9\.]([A-Za-z][A-Za-z0-9_]*) <- stripe_pattern\('
      r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _stripe_pattern(self, name, c1, c2):
    col1 = getattr(world, c1)
    col2 = getattr(world, c2)
    p = Stripe(col1, col2)
    setattr(world, name, p)


@step(r'[^a-z0-9\.]([A-Za-z][A-Za-z0-9_]*) <- gradient_pattern\('
      r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _gradient_pattern(self, name, c1, c2):
    col1 = getattr(world, c1)
    col2 = getattr(world, c2)
    p = Gradient(col1, col2)
    setattr(world, name, p)


@step(r'[^a-z0-9\.]([A-Za-z][A-Za-z0-9_]*) <- bigradient_pattern\('
      r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _bigradient_pattern(self, name, c1, c2):
    col1 = getattr(world, c1)
    col2 = getattr(world, c2)
    p = BiGradient(col1, col2)
    setattr(world, name, p)


@step(r'[^a-z0-9\.]([A-Za-z][A-Za-z0-9_]*) <- ring_pattern\('
      r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _ring_pattern(self, name, c1, c2):
    col1 = getattr(world, c1)
    col2 = getattr(world, c2)
    p = RingPattern(col1, col2)
    setattr(world, name, p)


@step(r'[^a-z0-9\.]([A-Za-z][A-Za-z0-9_]*) <- checkers_pattern\('
      r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _checkers_pattern(self, name, c1, c2):
    col1 = getattr(world, c1)
    col2 = getattr(world, c2)
    p = Checkers(col1, col2)
    setattr(world, name, p)


@step(r'[^a-z0-9\.]([A-Za-z][A-Za-z0-9_]*) <- ring_gradient_pattern\('
      r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _ring_gradient_pattern(self, name, c1, c2):
    col1 = getattr(world, c1)
    col2 = getattr(world, c2)
    p = RingGradient(col1, col2)
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
    col = pat.pattern_at(p)
    print("\nExpected:")
    print(c)
    print("\nGot:")
    print(col)
    assert col == c


@step(r'([A-Za-z][A-Za-z0-9_]*)\.pattern <- stripe_pattern\(colour'
      r'\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)'
      r'\s*,\s*colour\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\)\)')
def _set_material_stripe_pattern(self, name, r1, g1, b1, r2, g2, b2):
    m = getattr(world, name)
    c1 = Colour(float(r1), float(g1), float(b1))
    c2 = Colour(float(r2), float(g2), float(b2))
    m.pattern = Stripe(c1, c2)


@step(r'([A-Za-z][A-Za-z0-9_]*)\.pattern <- stripe_pattern\('
      r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _set_material_stripe_pattern_by_name(self, name, col1, col2):
    m = getattr(world, name)
    c1 = getattr(world, col1)
    c2 = getattr(world, col2)
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
    c = getattr(world, pattern).pattern_at(po)
    setattr(world, colour, c)


@step(r'colour ([A-Za-z][A-Za-z0-9_]*)\s*=\s*colour ([A-Za-z][A-Za-z0-9_]*)')
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
def _set_pattern_translation(self, name, tx, ty, tz):
    t = Translation(float(tx), float(ty), float(tz))
    getattr(world, name).transform = t


@step(r'([A-Za-z][A-Za-z0-9_]*) <- test_pattern\(\)')
def _test_pattern(self, name):
    setattr(world, name, TestPattern())


@step(r'([A-Za-z][A-Za-z0-9_]*) <- pattern_at_shape\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'point\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\)\)')
def _get_pattern_at_shape(self, colour, pattern, object, px, py, pz):
    pw = Point(float(px), float(py), float(pz))
    # Point is in world space, first transform to object space
    po = getattr(world, object).inverse_transform * pw
    # Pattern will handle the transform from object to pattern space
    c = getattr(world, pattern).pattern_at(po)
    setattr(world, colour, c)


@step(r'([A-Za-z][A-Za-z0-9_]*) <- solid_colour\(([A-Za-z][A-Za-z0-9_]*)\)')
def _solid_colour_by_name(self, name, colour):
    setattr(world, name, SolidColour(getattr(world, colour)))


@step(r'([A-Za-z][A-Za-z0-9_]*)\.(a|b)\s*=\s*solid_colour '
      r'([A-Za-z][A-Za-z0-9_]*)')
def _check_pattern_solid_colour(self, name, element, colour):
    p = getattr(world, name)
    c = getattr(world, colour)
    print("\nExpected:")
    print(c)
    print("\nGot:")
    print(getattr(p, element))
    assert getattr(p, element) == c


@step(r'pattern_at\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*point\(([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\)\s*=\s*'
      r'colour ([A-Za-z][A-Za-z0-9_]*)')
def _check_pattern_by_name(self, pattern, px, py, pz, col):
    pat = getattr(world, pattern)
    pos = Point(float(px), float(py), float(pz))
    tc = getattr(world, col)
    c = pat.pattern(pos)
    print("\nExpected:")
    print(tc)
    print("\nGot:")
    print(c)
    assert c == tc


@step(r'pattern_at\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*point\(([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)\)\s*=\s*'
      r'colour\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\)')
def _check_pattern_by_colour(self, pattern, px, py, pz, r, g, b):
    pat = getattr(world, pattern)
    pos = Point(float(px), float(py), float(pz))
    tc = Colour(float(r), float(g), float(b))
    c = pat.pattern(pos)
    print("\nExpected:")
    print(tc)
    print("\nGot:")
    print(c)
    assert c == tc
