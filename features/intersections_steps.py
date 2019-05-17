from aloe import world, step
from Intersection import Intersection
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
