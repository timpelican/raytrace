# Canvas for drawing on
# Bitmap is stored as a list of rows
# Each row is a list of Colours
# This means access is actually back to from from normal (x,y)
# and is in fact Canvas[y][x], but row first makes much more sense
# for rendering or writing to files

from Tuple4 import Colour


class Canvas(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = []
        for y in range(0, height):
            self.pixels.append([])
            for x in range(0, width):
                self.pixels[y].append(Colour(0, 0, 0))

    def pixel_at(self, x, y):
        p = self.pixels[y][x]
        return Colour(p.red, p.green, p.blue)

    def write_pixel(self, x, y, c):
        p = self.pixels[y][x]
        p.red = c.red
        p.green = c.green
        p.blue = c.blue

    def to_ppm(self):
        ppm_string = "P3\n"
        ppm_string += "{w} {h}\n".format(w=self.width, h=self.height)
        ppm_string += "255\n"
        for y in range(0, self.height):
            line = ""
            first = 1
            for x in range(0, self.width):
                p = self.pixels[y][x]
                red = max(0, min(255, int(round(p.red*255))))
                if len(line + " " + str(red)) > 70:
                    ppm_string += line + "\n"
                    line = ""
                    first = 1
                if first == 1:
                    first = 0
                else:
                    line += " "
                line += str(red)
                green = max(0, min(255, int(round(p.green*255))))
                if len(line + " " + str(green)) > 70:
                    ppm_string += line + "\n"
                    line = ""
                    first = 1
                if first == 1:
                    first = 0
                else:
                    line += " "
                line += str(green)
                blue = max(0, min(255, int(round(p.blue*255))))
                if len(line + " " + str(blue)) > 70:
                    ppm_string += line + "\n"
                    line = ""
                    first = 1
                if first == 1:
                    first = 0
                else:
                    line += " "
                line += str(blue)
            ppm_string += line + "\n"
        return ppm_string
