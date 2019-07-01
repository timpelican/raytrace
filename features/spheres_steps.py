from aloe import world, step
from Sphere import Sphere
from Matrix import IdentityMatrix
from maths import equals
from Tuple4 import Point, Colour
from Material import Material
import re
import Transformation

@step(r'([A-Za-z][A-Za-z0-9_]*) <- sphere\(\)$')
def _sphere(self, name):
    setattr(world, name, Sphere())


@step(r'([A-Za-z][A-Za-z0-9_]*) <- sphere\(\) with:')
def _sphere_with_values(self, name):
    s = Sphere()
    # TODO: feels like we should have a generic function for parsing
    # gherkin tables
    digit = re.compile(r'^[-+]?\d*\.?\d+$')
    tuple3 = re.compile(r'^\([-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\s*,\s*'
                        r'[-+]?\d*\.?\d+\)$')
    subattr = re.compile(r'.*\..*')
    scaling = re.compile(r'^scaling\([-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\s*,\s*'
                        r'[-+]?\d*\.?\d+\)$')
    for row in self.table:
        attr = str(row[0])
        obj = s
        print(obj, attr)
        while subattr.match(attr):
            print attr.split('.')
            obj = getattr(obj, attr.split('.', 2)[0])
            attr = attr.split('.', 2)[1]
            print(obj, attr)
        value = row[1]
        if digit.match(value):
            print("DIGIT", attr, float(value))
            setattr(obj, attr, float(value))
        if tuple3.match(value):
            values = value.replace("(", "").replace(")", "").split(',')
            print("TUPLE3", attr, float(values[0]), float(values[1]),
                  float(values[2]))
            setattr(obj, attr, Colour(float(values[0]), float(values[1]),
                                      float(values[2])))
        if scaling.match(value):
            values = value.split('(')[1].replace("(", "").replace(")", "").\
                split(',')
            print("SCALING", attr, Transformation.Scaling(float(values[0]),
                                                          float(values[1]),
                                                          float(values[2])))
            setattr(obj, attr, Transformation.Scaling(float(values[0]),
                                                      float(values[1]),
                                                      float(values[2])))
    setattr(world, name, s)


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
    assert equals(getattr(world, name)[int(index)], float(value))


@step(r'([A-Za-z][A-Za-z0-9_]*)\.transform equals the identity_matrix')
def _check_transform_identity(self, name):
    test_matrix = IdentityMatrix(4)
    print("\nExpected:")
    print(test_matrix)
    print("\nGot:")
    print(getattr(world, name).transform)
    assert getattr(world, name).transform == test_matrix


@step(r'set_transform\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9_]*)\)')
def _set_transform(self, obj, transform):
    getattr(world, obj).transform = getattr(world, transform)


@step(r'([A-Za-z][A-Za-z0-9_]*)\.transform\s*=\s*([A-Za-z][A-Za-z0-9_]*)')
def _check_transform_name(self, name1, name2):
    test_matrix = getattr(world, name2)
    print("\nExpected:")
    print(test_matrix)
    print("\nGot:")
    print(getattr(world, name1).transform)
    assert getattr(world, name1).transform == test_matrix


@step(r'([A-Za-z][A-Za-z0-9_]*) <- normal_at\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'point\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\)\)')
def _normal_at_point(self, name1, name2, x, y, z):
    p = Point(float(x), float(y), float(z))
    n = getattr(world, name2).normal_at(p)
    setattr(world, name1, n)


@step(r'([A-Za-z][A-Za-z0-9_]*) <- ([A-Za-z][A-Za-z0-9_]*)\.material')
def _get_material(self, name1, name2):
    setattr(world, name1, getattr(world, name2).material)


@step(r'material ([A-Za-z][A-Za-z0-9_]*) is the default material')
def _check_default_material(self, name):
    test_material = Material()
    print("\nExpected:")
    print(test_material)
    print("\nGot:")
    print(getattr(world, name))
    assert getattr(world, name) == test_material


@step(r'([A-Za-z][A-Za-z0-9_]*).ambient <- ([-+]?\d*\.?\d+)')
def _set_ambient(self, name, ambient):
    setattr(world, name, float(ambient))


@step(r'([A-Za-z][A-Za-z0-9_]*).material <- ([A-Za-z][A-Za-z0-9_]*)')
def _set_material(self, name1, name2):
    getattr(world, name1).material = getattr(world, name2)


@step(r'([A-Za-z][A-Za-z0-9_]*).material\s*=\s*([A-Za-z][A-Za-z0-9_]*)')
def _check_material(self, name1, name2):
    test_material = getattr(world, name2)
    print("\nExpected:")
    print(test_material)
    print("\nGot:")
    print(getattr(world, name1).material)
    assert getattr(world, name1).material == test_material
