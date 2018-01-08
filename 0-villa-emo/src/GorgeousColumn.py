from pyplasm import *

class GorgeousColumn:

    def __init__(self, dm, h):
        self.dm = float(dm)
        self.h = float(h)

    def render(self):
        """
        Columna

        :param dm: is the circumference diameter at the column basis;
        :param h: is the column height;
        :return:
        """
        cylndr = COMP([JOIN, TRUNCONE([self.dm / 2, .8 * self.dm / 2, self.h])])(24)
        torus_bot = COMP([JOIN, TORUS([self.dm / 12, self.dm / 2])])([8, 27])
        torus_top = COMP([JOIN, TORUS([.8 * (self.dm / 12), .8 * (self.dm / 2)])])([8, 24])
        base = COMP([T([1, 2])([7 * self.dm / -12, 7 * self.dm / -23]), CUBOID])([7 * self.dm / 6, 7 * self.dm / 6, self.dm / 6])
        base_top = COMP([T([1, 2])([7 * self.dm / -12, 7 * self.dm / -12]), CUBOID])([7 * self.dm / 6, 7 * self.dm / 6, self.dm / 6])
        capital = SUM([
            COMP([JOIN, TRUNCONE([.8 * self.dm / 2, 1.2 * self.dm / 2, self.h / 8])])(4),
            COMP([R([1, 2])(PI / 4), JOIN, TRUNCONE([.8 * self.dm / 2, 1.2 * self.dm / 2, self.h / 8])])(4)
        ])
        return TOP([TOP([TOP([TOP([TOP([base, torus_bot]), cylndr]), torus_top]), capital]), base_top])
