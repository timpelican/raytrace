from aloe import step, world
from World import World, DefaultWorld


@step(r'([A-Za-z][A-Za-z0-9_]*)\s*<-\s*world\(\)')
def _create_blank_world(self, name):
    setattr(world, name, World())


@step(r'([A-Za-z][A-Za-z0-9_]*) contains no objects')
def _world_has_no_objects(self, name):
    obj = getattr(world, name).objects
    print("\nExpected:")
    print("[]")
    print("\nGot:")
    print(obj)
    assert obj == []


@step(r'([A-Za-z][A-Za-z0-9_]*) has no light source')
def _world_has_no_lights(self, name):
    lights = getattr(world, name).lights
    print("\nExpected:")
    print("[]")
    print("\nGot:")
    print(lights)
    assert lights == []


@step(r'([A-Za-z][A-Za-z0-9_]*) <- default_world\(\)')
def _default_world(self, name):
    setattr(world, name, DefaultWorld())


@step(r'([A-Za-z][A-Za-z0-9_]*).lights\s*=\s*([A-Za-z][A-Za-z0-9_]*)')
def _check_light_by_name(self, name1, name2):
    lights = getattr(world, name1).lights
    print("\nExpected:")
    print([getattr(world, name2)])
    print("\nGot:")
    print(lights)
    assert lights == [getattr(world, name2)]


@step(r'([A-Za-z][A-Za-z0-9_]*) contains ([A-Za-z][A-Za-z0-9_]*)$')
def _check_contains_object(self, name1, name2):
    objects = getattr(world, name1).objects
    test_object = getattr(world, name2)
    print("\nExpected:")
    print(test_object)
    print("\nGot:")
    print(objects)
    found = False
    for o in objects:
        if o == test_object:
            found = True
    assert found is True


@step(r'([A-Za-z][A-Za-z0-9_]*) <- intersect_world\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _intersect_world(self, name1, name2, name3):
    w = getattr(world, name2)
    r = getattr(world, name3)
    i = w.intersections(r)
    setattr(world, name1, i)


@step(r'([A-Za-z][A-Za-z0-9_]*) <- the first object in '
      r'([A-Za-z][A-Za-z0-9_]*)')
def _first_world_object(self, name1, name2):
    setattr(world, name1, getattr(world, name2).objects[0])


@step(r'([A-Za-z][A-Za-z0-9_]*) <- the second object in '
      r'([A-Za-z][A-Za-z0-9_]*)')
def _second_world_object(self, name1, name2):
    setattr(world, name1, getattr(world, name2).objects[1])


@step(r'([A-Za-z][A-Za-z0-9_]*) <- shade_hit\(([A-Za-z][A-Za-z0-9_]*)'
      r'\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _get_shade_hit(self, name1, name2, name3):
    w = getattr(world, name2)
    c = getattr(world, name3)
    setattr(world, name1, w.shade_hit(c))


@step(r'([A-Za-z][A-Za-z0-9_]*)\.light <- ([A-Za-z][A-Za-z0-9_]*)')
def _set_light_by_name(self, name1, name2):
    # Replace the World light array with a new light
    w = getattr(world, name1)
    light = getattr(world, name2)
    w.lights = [light]
