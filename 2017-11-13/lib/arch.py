from pyplasm import MAP, MULTEXTRUDE, PROD, INTERVALS, TRUE, PI, T
import math


def arch(rr=5, w=1, depth=1, a=1, b=1, half=TRUE):
    """
    Arcata parametrizzabile

    :param rr: raggio maggiore
    :param w: raggio minore
    :param depth: spessore
    :param a: schiacciamento
    :param b: allungamento
    :param half: arco (default TRUE) o circolare
    :return:
    """
    y = lambda (p, q): a * q * math.sin(p)
    x = lambda (p, q): b * q * math.cos(p)

    numberOfPI = 1 if half else 2

    dom2D = MAP([x, y])(T(2)(rr)(PROD([INTERVALS(numberOfPI * PI)(24), INTERVALS(w)(1)])))
    dom3D = MULTEXTRUDE(dom2D)(depth)
    return dom3D
