from aloe import step, world
from World import World


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
