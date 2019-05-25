from aloe import world, step
from Intersection import Intersection, Intersections
from maths import equals


@step(r'([A-Za-z][A-Za-z0-9]*) <- intersection\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9]*)\)')
def _intersection(self, name1, t, name2):
    setattr(world, name1, Intersection(float(t), getattr(world, name2)))


@step(r'([A-Za-z][A-Za-z0-9]*)\.t\s*=\s*([-+]?\d*\.?\d+)')
def _check_t_value(self, name, value):
    test_value = float(value)
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(getattr(world, name).t)
    assert equals(getattr(world, name).t, test_value)


@step(r'([A-Za-z][A-Za-z0-9]*)\.object\s*=\s*([A-Za-z][A-Za-z0-9]*)')
def _check_object_name(self, name1, name2):
    test_object = getattr(world, name2)
    print("\nExpected:")
    print(test_object)
    print("\nGot:")
    print(getattr(world, name1))
    assert getattr(world, name1).object == test_object


@step(r'([A-Za-z][A-Za-z0-9]*) <- intersections\(([A-Za-z][A-Za-z0-9]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9]*)\)')
def _intersections2(self, name, i1, i2):
    setattr(world, name, Intersections(getattr(world, i1), getattr(world, i2)))


@step(r'([A-Za-z][A-Za-z0-9]*) <- intersections\(([A-Za-z][A-Za-z0-9]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9]*)\s*,\s*([A-Za-z][A-Za-z0-9]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9]*)\)')
def _intersections4(self, name, i1, i2, i3, i4):
    setattr(world, name, Intersections(getattr(world, i1), getattr(world, i2),
                                       getattr(world, i3), getattr(world, i4)))


@step(r'([A-Za-z][A-Za-z0-9]*)\[(\d+)\]\.t\s*=\s*([-+]?\d*\.?\d+)')
def _check_intersections_t_value(self, name, index, value):
    test_value = float(value)
    test_index = int(index)
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(getattr(world, name)[test_index].t)
    assert equals(getattr(world, name)[test_index].t, test_value)


@step(r'([A-Za-z][A-Za-z0-9]*)\[(\d+)\]\.object\s*=\s*([A-Za-z][A-Za-z0-9]*)')
def _check_intersections_object_name(self, name1, index, name2):
    test_object = getattr(world, name2)
    test_index = int(index)
    print("\nExpected:")
    print(test_object)
    print("\nGot:")
    print(getattr(world, name1)[test_index].object)
    assert getattr(world, name1)[test_index].object == test_object


@step(r'([A-Za-z][A-Za-z0-9]*) <- hit\(([A-Za-z][A-Za-z0-9]*)\)')
def _hit(self, name1, name2):
    setattr(world, name1, getattr(world, name2).hit())


@step(r'hit ([A-Za-z][A-Za-z0-9]*)\s*=\s*([A-Za-z][A-Za-z0-9]*)')
def _check_hit(self, name1, name2):
    test_object = getattr(world, name2)
    print("\nExpected:")
    print(test_object)
    print("\nGot:")
    print(getattr(world, name1))
    assert getattr(world, name1) == test_object


@step(r'hit ([A-Za-z][A-Za-z0-9]*) is nothing')
def _check_hit_nothing(self, name):
    print("\nExpected:")
    print("None")
    print("\nGot:")
    print(getattr(world, name))
    assert getattr(world, name) is None
