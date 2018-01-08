from pyplasm import *


class Arch:

    def __init__(self, lateral_width, height, deep):
        self.lateral_width = float(lateral_width)
        self.height = float(height)
        self.deep = float(deep)

    def render(self):
        def bottomArc(d):
            return BEZIER(S1)([[0, 0], [0, 2 * d / 3], [d, 2 * d / 3], [d, 0]])

        def topArc(d):
            return BEZIER(S1)([[0, 2 * d / 3], [d, 2 * d / 3]])

        def arc2D(d):
            return BEZIER(S2)([bottomArc(d), topArc(d)])

        def arc3D(d):
            def arc3D1(w):
                arco = arc2D(d)
                dominio = PROD([INTERVALS(1)(8), INTERVALS(1)(1)])
                ar = MAP(arco)(dominio)
                domin = PROD([ar, QUOTE([1.5])])
                return COMP([T(2)(w), R([2, 3])(PI / 2)])(domin)

            return arc3D1

        def Interarc(d1, d2):
            def Interarc1(w):
                return CUBOID([d1, w, 2 * d2 / 3])

            return Interarc1

        def Xarc(d1, d2):
            def Xarc1(w):
                return RIGHT([RIGHT([Interarc(d1, d2)(w), arc3D(d2)(w)]), Interarc(d1, d2)(w)])

            return Xarc1

        return Xarc(self.lateral_width, self.height)(self.deep)
