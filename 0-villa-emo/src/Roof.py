from pyplasm import *


class Roof:

    def __init__(self, width, depth, height):
        self.width = float(width)
        self.scale = float(depth/width)
        self.height = float(height)

    def render(self):
        return SCALE(2)(self.scale)(ROTATE([1, 2])(PI/4)(CONE([self.width, self.height])(4)))
