from aloe import world, step
from Intersection import Intersection, Intersections
from maths import equals
from Tuple4 import Point, Vector


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


@step(r'([A-Za-z][A-Za-z0-9]*)\.object\s*=\s*object\*([A-Za-z][A-Za-z0-9]*)')
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


@step(r'([A-Za-z][A-Za-z0-9]*)\[(\d+)\]\.object\s*=\s*object\s*'
      r'([A-Za-z][A-Za-z0-9]*)')
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


@step(r'([A-Za-z][A-Za-z0-9]*) <- prepare_computations\(([A-Za-z][A-Za-z0-9]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9]*)\)')
def _prepare_computations(self, name1, name2, name3):
    i = getattr(world, name2)
    r = getattr(world, name3)
    setattr(world, name1, i.prepare_computations(r))


@step(r'([A-Za-z][A-Za-z0-9]*)\.t\s*=\s*([A-Za-z][A-Za-z0-9]*)\.t')
def _compare_t_by_name(self, name1, name2):
    test_value = getattr(world, name2).t
    value = getattr(world, name1).t
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(value)
    assert value == test_value


@step(r'([A-Za-z][A-Za-z0-9]*)\.object\s*=\s*([A-Za-z][A-Za-z0-9]*)\.object')
def _compare_object_by_name(self, name1, name2):
    test_value = getattr(world, name2).object
    value = getattr(world, name1).object
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(value)
    assert value == test_value


@step(r'([A-Za-z][A-Za-z0-9]*)\.object\s*=\s*object\s*([A-Za-z][A-Za-z0-9]*)')
def _compare_object_by_direct_name(self, name1, name2):
    test_value = getattr(world, name2)
    value = getattr(world, name1).object
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(value)
    assert value == test_value


@step(r'([A-Za-z][A-Za-z0-9]*)\.point\s*=\s*point\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _compare_point_by_value(self, name, x, y, z):
    test_value = Point(float(x), float(y), float(z))
    value = getattr(world, name).point
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(value)
    assert value == test_value


@step(r'([A-Za-z][A-Za-z0-9]*)\.eyev\s*=\s*vector\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _compare_eyev_by_value(self, name, x, y, z):
    test_value = Vector(float(x), float(y), float(z))
    value = getattr(world, name).eyev
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(value)
    assert value == test_value


@step(r'([A-Za-z][A-Za-z0-9]*)\.normalv\s*=\s*vector\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _compare_normalv_by_value(self, name, x, y, z):
    test_value = Vector(float(x), float(y), float(z))
    value = getattr(world, name).normalv
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(value)
    assert value == test_value


@step(r'([A-Za-z][A-Za-z0-9]*)\.inside is (true|false)')
def _check_inside(self, name, truefalse):
    if truefalse == "true":
        test_value = True
    else:
        test_value = False
    value = getattr(world, name).inside
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(value)
    assert value == test_value


@step(r'([A-Za-z][A-Za-z0-9]*).over_point.([xyz])\s*<\s*([-+]?\d*\.?\d+)')
def _over_point_lt(self, name, xyz, value):
    test_value = float(value)
    op = getattr(world, name).over_point
    opxyz = getattr(op, xyz)
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(opxyz)
    assert opxyz < test_value


@step(r'([A-Za-z][A-Za-z0-9]*).point.([xyz])\s*>\s*'
      r'([A-Za-z][A-Za-z0-9]*).over_point.([xyz])')
def _point_gt_over_point(self, name1, xyz1, name2, xyz2):
    p = getattr(world, name1).point
    value = getattr(p, xyz1)
    op = getattr(world, name2).over_point
    test_value = getattr(op, xyz2)
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(value)
    assert value > test_value


@step(r'([A-Za-z][A-Za-z0-9]*)\.reflectv\s*=\s*vector\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _compare_reflectv_by_value(self, name, x, y, z):
    test_value = Vector(float(x), float(y), float(z))
    value = getattr(world, name).reflectv
    print("\nExpected:")
    print(test_value)
    print("\nGot:")
    print(value)
    assert value == test_value
