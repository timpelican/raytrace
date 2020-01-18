from aloe import world, step
from Plane import Plane
from Tuple4 import Point, Colour
import re
import Transformation


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


@step(r'([A-Za-z][A-Za-z0-9_]*) <- plane\(\) with:')
def _plane_with_values(self, name):
    p = Plane()
    # TODO: feels like we should have a generic function for parsing
    # gherkin tables
    digit = re.compile(r'^[-+]?\d*\.?\d+$')
    tuple3 = re.compile(r'^\([-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\s*,\s*'
                        r'[-+]?\d*\.?\d+\)$')
    subattr = re.compile(r'.*\..*')
    translation = re.compile(r'^translation\([-+]?\d*\.?\d+\s*,\s*'
                             r'[-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\)$')
    for row in self.table:
        attr = str(row[0])
        obj = p
        print(obj, attr)
        while subattr.match(attr):
            print(attr.split('.'))
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
        if translation.match(value):
            values = value.split('(')[1].replace("(", "").replace(")", "").\
                split(',')
            print("TRANS", attr, float(values[0]), float(values[1]),
                  float(values[2]))
            setattr(obj, attr, Transformation.Translation(float(values[0]),
                                                          float(values[1]),
                                                          float(values[2])))
    setattr(world, name, p)
