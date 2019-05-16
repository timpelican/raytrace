#!/usr/bin/env python
from Tuple4 import Point, Colour
import Canvas
import math


def plot(canvas, point, colour):
    x = int((canvas.width/2) + round(point.x))
    y = int((canvas.height/2) - round(point.y))
    c.write_pixel(x, y, colour)


def plot_cross(canvas, point, colour):
    x = int((canvas.width/2) + round(point.x))
    y = int((canvas.height/2) - round(point.y))
    c.write_pixel(x, y, colour)
    c.write_pixel(x+1, y, colour)
    c.write_pixel(x-1, y, colour)
    c.write_pixel(x, y+1, colour)
    c.write_pixel(x, y-1, colour)


white = Colour(0.8, 0.8, 0.8)
c = Canvas.Canvas(600, 600)
p = Point(0, 250, 0)

for r in range(0, 12):
    p2 = p.rotate_z(-r * math.pi / 6)
    plot_cross(c, p2, white)
c.to_ppm_file("clock.ppm")
