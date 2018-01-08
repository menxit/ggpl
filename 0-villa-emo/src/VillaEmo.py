from pyplasm import *
import Factory
from Steps import Steps
from Column import Column
from GorgeousColumn import GorgeousColumn
from Triangle import Triangle
from Roof import Roof
from Arch import Arch
import os

path = os.path.dirname(__file__)


class VillaEmo:
    def __init__(self):
        self.planimetry = Factory.create_planimetry()
        self.column = Factory.create_column()
        self.gorgeous_column = GorgeousColumn(5, 18)
        self.top_triangle = Triangle(42, 10)
        self.lateral_roof = Triangle(52, 201)
        self.main_roof = Roof(72, 65.16, 16)
        self.arch = Arch(4, 15, 1.5)

    def render(self):
        return STRUCT([
            self.get_top_triangle(),
            self.get_planimetry(),
            self.get_steps(),
            self.texture("intonaco.jpg", 5, 5)(TOP([self.get_columns_lx(), self.get_archs()])),
            self.texture("intonaco.jpg", 5, 5)(TOP([self.get_columns_rx(), self.get_archs()])),
            self.get_first_floor(),
            self.get_gorgeous_columns(),
            self.get_lateral_roof(),
            self.get_main_root(),
            self.lateral_floor(),
        ])

    def get_planimetry(self):
        return self.texture("intonaco.jpg", .5, .5)(DIFFERENCE([
            self.planimetry.render(),
            self.get_entrance()
        ]))

    def get_steps(self):
        steps = Steps(steps=20, width=45, height=15, depth=84)
        return T([1, 2, 3])([229, 0, 0])(self.texture("steps.jpg", .5, .5)(steps.render()))

    def get_columns_lx(self):
        column = self.get_column()
        return T([1, 2])([0, 90])(STRUCT(self.repeat(column, 1, 12, 17.7)))

    def get_columns_rx(self):
        column = self.get_column()
        return T([1, 2])([301, 90])(STRUCT(self.repeat(column, 1, 12, 17.7)))

    def get_column(self):
        return Column(width=6, height=19, width_decoration=7, height_decoration=1).render()

    def get_entrance(self):
        return T([1, 2, 3])([233, 83, 16])(CUBOID([36, 2, 25]))

    def get_first_floor(self):
        return T([1, 2, 3])([202, 84, 15])(self.texture("atrio.jpg", 1.5, 1.5)(CUBOID([94, 84, 1])))

    def get_gorgeous_columns(self):
        gorgeous_column = self.texture("intonaco.jpg", .5, .5)(self.gorgeous_column.render())
        return T([1, 2, 3])([233, 83, 16])(STRUCT(self.repeat(gorgeous_column, 1, 4, 12)))

    def get_top_triangle(self):
        height_base = 9
        return T([1, 2, 3])([230, 108, 41])((STRUCT([
            T(2)(-26)(self.texture("intonaco.jpg", 5, 5)(CUBOID([42, 5, height_base]))),
            self.texture("tegole.jpg", 1, 2)(T(3)(height_base)(Triangle(42, 27).render())),
            T([2, 3])([-26.5, height_base])(self.texture("fronte.jpg", 35., 31.)(Triangle(42, 1).render())),
        ])))

    def get_lateral_roof(self):
        roof = self.texture("tegole.jpg", .5, .5)(self.lateral_roof.render())
        return STRUCT(self.repeat(
            T([1, 2, 3])([0, 93, 30])(ROTATE([1, 2])(PI / 2)(roof)), 1, 2, 301))

    def get_main_root(self):
        return T([1, 2, 3])([251, 129, 50])(self.texture("tegole.jpg", .5, .5)(self.main_roof.render()))

    def get_archs(self):
        arch = self.arch.render()
        return STRUCT(self.repeat(arch, 1, 11, 17.7))

    def texture(self, f, scale_x=0, scale_y=0):
        return TEXTURE([
                           os.path.join(path, "../assets/" + f)] +
                       [True, True, 0.0, 0.0, 0.0, 1+float(1/scale_x), 1+float(1/scale_y), 0.0, 0.0])

    def lateral_floor(self):
        pav = self.texture("pavimento.jpg", 1, 1)(QUOTE([200, 13, 1]))
        return T(2)(92)(STRUCT(self.repeat(pav, 1, 10, 10)))

    @staticmethod
    def repeat(o, axis, n, space):
        return map(lambda i: T(axis)(i * space)(o), range(0, n))
