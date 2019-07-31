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
