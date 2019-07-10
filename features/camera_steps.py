from aloe import step, world
from Camera import Camera
from Matrix import IdentityMatrix
from maths import equals
from Transformation import Rotation_y, Translation, ViewTransform


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


@step(r'([A-Za-z][A-Za-z0-9_]*) <- camera\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _camera_by_values(self, name1, hsize, vsize, fov):
    setattr(world, name1, Camera(float(hsize), float(vsize),
                                 float(fov)))


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
    assert equals(fov, test_fov)


@step(r'([A-Za-z][A-Za-z0-9]*).transform is the identity_matrix')
def _check_identity_matrix(self, name):
    id = IdentityMatrix(getattr(world, name).transform.rows)
    print("Expected:")
    print(id)
    print("\nGot:")
    print(getattr(world, name).transform)
    assert getattr(world, name).transform == id


@step(r'([A-Za-z][A-Za-z0-9]*)\.pixel_size\s*=\s*(\d*\.?\d+)')
def _check_pixel_size(self, name, size):
    test_size = float(size)
    actual_size = getattr(world, name).pixel_size
    print("Expected:")
    print(test_size)
    print("\nGot:")
    print(actual_size)
    assert equals(actual_size, test_size)


@step(r'([A-Za-z][A-Za-z0-9]*) <- ray_for_pixel\(([A-Za-z][A-Za-z0-9]*)\s*,\s*'
      r'(\d+)\s*,\s*(\d+)\)')
def _ray_for_pixel(self, name1, name2, value1, value2):
    px = int(value1)
    py = int(value2)
    c = getattr(world, name2)
    setattr(world, name1, c.ray_for_pixel(px, py))


@step(r'camera ([A-Za-z][A-Za-z0-9]*) has transform rotation_y\('
      r'([-+]?\d*\.?\d+)\)\s*\*\s*translation\(([-+]?\d*\.?\d+)\s*,\s*'
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
def _transform_camera(self, name, ry, tx, ty, tz):
    t = Rotation_y(float(ry)) * Translation(float(tx), float(ty), float(tz))
    getattr(world, name).transform = t


@step(r'camera ([A-Za-z][A-Za-z0-9]*) has view_transform\('
      r'([A-Za-z][A-Za-z0-9]*)\s*,\s*([A-Za-z][A-Za-z0-9]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9]*)\)')
def _camera_view_transform(self, name1, name2, name3, name4):
    p_from = getattr(world, name2)
    p_to = getattr(world, name3)
    v_up = getattr(world, name4)
    getattr(world, name1).transform = ViewTransform(p_from, p_to, v_up)


@step(r'([A-Za-z][A-Za-z0-9]*) <- render_world\(([A-Za-z][A-Za-z0-9]*)\s*,\s*'
      r'([A-Za-z][A-Za-z0-9]*)\)')
def _render_image(self, name1, name2, name3):
    c = getattr(world, name2)
    w = getattr(world, name3)
    setattr(world, name1, c.render_world(w))
