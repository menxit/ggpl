from pyplasm import *
from larlib import *
from Utilities import *


class Triangle:
    assets = []

    def __init__(self, width, depth):
        self.width = float(width)
        self.depth = float(depth)

    def render(self):
        return ROTATE([2, 3])(PI/2)(MULTEXTRUDE(MKPOL([
            [[0, 0], [self.width/2, self.width/4], [self.width, 0]],
            [[1, 2, 3]],
            None]))(self.depth))
