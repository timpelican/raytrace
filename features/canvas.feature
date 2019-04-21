Feature: Canvas operations

As a programmer
I want to be able to draw on a canvas
So I can see the output of my ray-tracer


Scenario: Creating a canvas
  Given c <- canvas(10, 20)
  Then c.width = 10
  And c.height = 20
  And every pixel of c is colour(0, 0, 0)

Scenario: Writing pixels to a canvas
  Given c <- canvas(10, 20)
  And red <- colour(1, 0, 0)
  When write_pixel(c, 2, 3, red)
  Then pixel_at(c, 2, 3) = red

Scenario: Constructing the PPM header
  Given c <- canvas(5, 3)
  When ppm <- canvas_to_ppm(c)
  Then lines 1-3 of ppm are
    """
    P3
    5 3
    255
    """

Scenario: Constructing the PPM pixel data
  Given c <- canvas(5, 3)
  And c1 <- colour(1.5, 0, 0)
  And c2 <- colour(0, 0.5, 0)
  And c3 <- colour(-0.5, 0, 1)
  When write_pixel(c, 0, 0, c1)
  And write_pixel(c, 2, 1, c2)
  And write_pixel(c, 4, 2, c3)
  And ppm <- canvas_to_ppm(c)
  Then lines 4-6 of ppm are
    """
    255 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 128 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 255
    """
