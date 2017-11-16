from pyplasm import *


def HEMISPHERE(radius):
    """
    Hemisphere
    :param radius:
    :return:
    """
    def HEMISPHERE1 (subds):
        N, M = subds
        domain = Plasm.translate( Plasm.power(INTERVALS(PI/2)(N), INTERVALS(2*PI)(M)), Vecf(0, -PI/2, 0))
        fx = lambda p: radius * math.cos(p[0]) * math.sin(p[1])
        fy = lambda p: radius * math.cos(p[0]) * math.cos(p[1])
        fz = lambda p: radius * math.sin(p[0])
        ret = MAP([fx, fy, fz])(domain)
        return ret
    return HEMISPHERE1


def church(base=1, numberOfColumns=8, ratio=.809):
    """
    Returns a PyPlams object that models a church.
    :param base:
    :param ratio:
    :param numberOfColumns:
    :return:
    """

    def centeredCuboid(a, b, c):
        """
        Returns a centered CUBOID
        :param a:
        :param b:
        :param c:
        :return:
        """
        return T([1, 2])([-float(b)/2, -float(b)/2])(CUBOID([a, b, c]))

    def getHemisphere():
        """
        Returns an hemisphere
        :return:
        """
        return R([1, 3])(-PI)(HEMISPHERE(1)([8, 8]))

    def arrangedCircularly(o, r, n=numberOfColumns):
        """
        Arranges circularly a PyPlasm object
        :param o:
        :param r:
        :param n:
        :return:
        """
        return STRUCT(map(lambda i: T([1, 2])([
            r*math.cos((2 * PI / n) * i),
            r*math.sin((2 * PI / n) * i)
        ])(R([1, 2])((2 * PI / n) * i)(o)), range(0, n)))

    def getCylinder():
        """
        Returns a decorated and colored cylinder
        :return:
        """
        c1 = "#878787"
        c2 = "#afafaf"
        c3 = "#cecece"
        c4 = "#e8e8e8"
        c5 = "#5c1b1b"
        return STRUCT([
            HEX(c1)(T(3)(ratio - .05)(CYLINDER([1.05, .05])(8))),
            HEX(c2)(T(3)(ratio - .1)(CYLINDER([1.025, .05])(8))),
            HEX(c3)(T(3)(ratio - .15)(CYLINDER([1.0125, .05])(8))),
            HEX(c4)(DIFFERENCE([
                CYLINDER([1, ratio - .15])(8),
                CYLINDER([.9, ratio - .15])(8),
                HEX(c5)(
                    T(3)(.075)(R([1, 2])(PI / 8)(arrangedCircularly(centeredCuboid(.08, PI / 8, ratio - 0.3), 1.05, 8)))),
            ])),
            HEX(c5)(T(3)(.075)(R([1, 2])(PI / 8)(arrangedCircularly(centeredCuboid(.04, PI / 8, ratio - 0.3), 1.05, 8)))),
        ])

    def getColumn():
        """
        Returns a cylinder with a hemisphere over it.
        :return:
        """
        cylinder = getCylinder()
        return STRUCT([
            cylinder,
            HEX("#5C1B1B")(T(3)(ratio)(getHemisphere()))
        ])

    def render():
        return STRUCT([

            # scalini
            T(3)(0.000)(S([1, 2])([1.00, 1.00])(CYLINDER([1, 0.025])(8))),
            T(3)(0.025)(S([1, 2])([0.95, 0.95])(CYLINDER([1, 0.025])(8))),
            T(3)(0.050)(S([1, 2])([0.90, 0.90])(CYLINDER([1, 0.025])(8))),

            # base
            T(3)(0.075)(S([1, 2, 3])([.85, .85, .85])(getCylinder())),

            # cupola centrale
            T(3)(0.075 + ratio * .85)(S([1, 2, 3])([.425, .425, .425])(getColumn())),

            # cupole laterali 0,2125
            T(3)(0.075 + ratio * .85)(arrangedCircularly(S([1, 2, 3])([.2125, .2125, .2125])(getColumn()), .425 + .2125)),

        ])

    return S([1, 2, 3])([base, base, base])(render())
