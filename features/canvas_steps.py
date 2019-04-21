from aloe import step, world
from Canvas import Canvas
from maths import equals
from Tuple4 import Colour


@step(r'(\S+) <- canvas\s*\((\d+),\s*(\d+)\)')
def _c_is_a_canvas(self, name, width, height):
    setattr(world, name, Canvas(int(width), int(height)))


@step(r'(\S+)\.(width|height)\s*=\s*(\d+)')
def _canvas_member_equals(self, name, member, value):
    assert equals(getattr(getattr(world, name), member), int(value))


@step(r'every pixel of (\S+) is colour\(([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+),'
      r'\s*([-+]?\d*\.?\d+)\)')
def _canvas_one_colour(self, name, red, green, blue):
    test_colour = Colour(float(red), float(green), float(blue))
    canvas = getattr(world, name)
    for x in range(0, canvas.width):
        for y in range(0, canvas.height):
            assert canvas.pixel_at(x, y) == test_colour


@step(r'write_pixel\((\S+),\s*(\d+),\s*(\d+),\s*(\S+)\)')
def _write_pixel_name(self, name, x, y, colour):
    getattr(world, name).write_pixel(int(x), int(y), getattr(world, colour))


@step(r'pixel_at\((\S+),\s*(\d+),\s*(\d+)\)\s*=\s*(\S+)')
def _pixel_at_name(self, name, x, y, colour):
    test_canvas = getattr(world, name)
    test_colour = getattr(world, colour)
    assert test_canvas.pixel_at(int(x), int(y)) == test_colour


@step(r'(\S+) <- canvas_to_ppm\((\S+)\)')
def _canvas_to_ppm(self, name, canvas):
    setattr(world, name, getattr(world, canvas).to_ppm())


@step(r'lines (\d+)-(\d+) of (\S+) are')
def _compare_mls_range(self, first, last, name):
    test_string = self.multiline
    test_range = getattr(world, name).splitlines()
    test_mls = "\n".join(test_range[int(first)-1:int(last)])
    print "Expected\n", test_string, "\n\nGot\n", test_mls
    assert test_mls == test_string
