from aloe import world, step
from Plane import Plane
from Tuple4 import Point


@step(r'([A-Za-z][A-Za-z0-9_]*) <- plane\(\)$')
def _plane(self, name):
    setattr(world, name, Plane())


@step(r'([A-Za-z][A-Za-z0-9_]*) <- local_normal_at\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*point\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\)')
def _local_normal_at(self, name1, name2, px, py, pz):
    p = Point(float(px), float(py), float(pz))
    o = getattr(world, name2)
    setattr(world, name1, o.local_normal_at(p))

@step(r'([A-Za-z][A-Za-z0-9_]*) <- local_intersects\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _local_intersects(self, name1, name2, name3):
    o = getattr(world, name2)
    r = getattr(world, name3)
    setattr(world, name1, o.local_intersects(r))


@step('([A-Za-z][A-Za-z0-9_]*) is empty')
def _is_empty(self, name):
    print("\nExpected:")
    print("[]")
    print("\nGot:")
    print(getattr(world, name))
    assert len(getattr(world, name)) == 0
