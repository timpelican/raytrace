from aloe import world, step
from Sphere import Sphere


@step(r'([A-Za-z][A-Za-z0-9_]*) <- sphere\(\)')
def _sphere(self, name):
    setattr(world, name, Sphere())


@step(r'([A-Za-z][A-Za-z0-9_]*) <- intersect\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _intersects(self, name1, name2, name3):
    setattr(world, name1,
            getattr(world, name2).intersects(getattr(world, name3)))


@step(r'([A-Za-z][A-Za-z0-9_]*).count\s*=\s*(\d+)')
def _count_equals_value(self, name, value):
    print("\nExpected:")
    print(int(value))
    print("\nGot:")
    print(len(getattr(world, name)))
    assert len(getattr(world, name)) == int(value)


@step(r'([A-Za-z][A-Za-z0-9_]*)\[(\d+)\]\s*=\s*([-+]?\d*\.?\d+)')
def _index_equals_value(self, name, index, value):
    print("\nExpected:")
    print(float(value))
    print("\nGot:")
    print(getattr(world, name)[int(index)])
