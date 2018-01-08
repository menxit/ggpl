from pyplasm import *


class Column:

    def __init__(self, width, height, width_decoration, height_decoration):
        self.width = float(width)
        self.height = float(height)
        self.width_decoration = float(width_decoration)
        self.height_decoration = float(height_decoration)

    def render(self):
        return STRUCT([
            T(3)(self.height)(self._get_base()),
            CUBOID([self.width, self.width, self.height]),
            T(3)(0)(self._get_base()),
        ])

    def _get_base(self):
        translation = -(self.width_decoration-self.width)/2
        return T([1, 2])([translation, translation])(CUBOID([
            self.width_decoration,
            self.width_decoration,
            self.height_decoration
        ]))
