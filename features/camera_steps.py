from aloe import step, world
from Camera import Camera
from Matrix import IdentityMatrix


@step(r'(hsize|vsize) <- (\d+)')
def _set_size(self, name, value):
    setattr(world, name, int(value))


@step(r'(field_of_view) <- (\d*\.?\d+)')
def _set_fov(self, name, value):
    setattr(world, name, float(value))


@step(r'([A-Za-z][A-Za-z0-9_]*) <- camera\(([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\)')
def _camera_by_names(self, name1, name2, name3, name4):
    hsize = getattr(world, name2)
    vsize = getattr(world, name3)
    fov = getattr(world, name4)
    setattr(world, name1, Camera(hsize, vsize, fov))


@step(r'([A-Za-z][A-Za-z0-9_]*).(hsize|vsize)\s*=\s*(\d+)')
def _check_size(self, name, attr, value):
    test_size = int(value)
    size = getattr(getattr(world, name), attr)
    print("\nExpected:")
    print(test_size)
    print("\nGot:")
    print(size)
    assert size == test_size


@step(r'([A-Za-z][A-Za-z0-9_]*).(field_of_view)\s*=\s*(\d*\.?\d+)')
def _check_fov(self, name, attr, value):
    test_fov = float(value)
    fov = getattr(getattr(world, name), attr)
    print("\nExpected:")
    print(test_fov)
    print("\nGot:")
    print(fov)
    assert fov == test_fov


@step(r'([A-Za-z][A-Za-z0-9]*).transform is the identity_matrix')
def _check_identity_matrix(self, name):
    id = IdentityMatrix(getattr(world, name).transform.rows)
    print("Expected:")
    print(id)
    print("\nGot:")
    print(getattr(world, name).transform)
    assert getattr(world, name).transform == id
