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
