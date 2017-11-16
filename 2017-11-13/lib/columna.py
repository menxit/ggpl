from pyplasm import COMP, TRUNCONE, JOIN, TORUS, CUBOID, TOP, T, R, SUM, PI


def columna(dm, h):
    """
    Columna

    :param dm: is the circumference diameter at the column basis;
    :param h: is the column height;
    :return:
    """
    cylndr = COMP([JOIN, TRUNCONE([dm / 2, .8 * dm / 2, h])])(24)
    torus_bot = COMP([JOIN, TORUS([dm / 12, dm / 2])])([8, 27])
    torus_top = COMP([JOIN, TORUS([.8 * (dm / 12), .8 * (dm / 2)])])([8, 24])
    base = COMP([T([1, 2])([7 * dm / -12, 7 * dm / -23]), CUBOID])([7 * dm / 6, 7 * dm / 6, dm / 6])
    base_top = COMP([T([1, 2])([7 * dm / -12, 7 * dm / -12]), CUBOID])([7 * dm / 6, 7 * dm / 6, dm / 6])
    capital = SUM([
        COMP([JOIN, TRUNCONE([.8 * dm / 2, 1.2 * dm / 2, h / 8])])(4),
        COMP([R([1, 2])(PI / 4), JOIN, TRUNCONE([.8 * dm / 2, 1.2 * dm / 2, h / 8])])(4)
    ])
    return TOP([TOP([TOP([TOP([TOP([base, torus_bot]), cylndr]), torus_top]), capital]), base_top])
