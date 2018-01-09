from larlib import *
import os
import random
from datetime import date, datetime
import numpy

def get_season(now):
    Y = 2000
    seasons = [(3, (date(Y, 1, 1), date(Y, 3, 20))),
               (0, (date(Y, 3, 21), date(Y, 6, 20))),
               (1, (date(Y, 6, 21), date(Y, 9, 22))),
               (2, (date(Y, 9, 23), date(Y, 12, 20))),
               (3, (date(Y, 12, 21), date(Y, 12, 31)))]
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)

SEASON = get_season(date.today())

__dir = os.path.dirname(__file__)

EMPTY = CUBOID([0])
MIDDLE = ALIGN([[1, MED, MED], [2, MED, MED], [3, MIN, MIN]])

def texture(f, scale_x=1., scale_y=1.):
    _scale_x = float(scale_x)
    _scale_y = float(scale_y)
    print os.path.dirname(__file__) + "./assets/" + f
    return TEXTURE([
        os.path.join(os.path.dirname(__file__), "assets/" + f),
        True, True, 1.0, 1.0, 0.0, scale_x, scale_x, 0.0, 0.0
    ])


def tegole(scale_x=2, scale_y=2):
    return texture("tegole.jpg", scale_x, scale_y)

def intonaco():
    return texture("intonaco.jpg")


def cespugli(depth, height, N):
    cespuglio = texture("1.jpg")(CUBOID([depth, depth, height]))
    return STRUCT(map(lambda x : T([2, 3])([x*depth, x*height])(cespuglio), range(0, N)))

def tetto_piramidale(depth, width, height):
    """
    Crea un tetto a punta

    :param width:
    :param depth:
    :param height:
    :return:
    """
    _width = float(width)
    _scale = float(depth) / _width
    _height = float(height)
    return SCALE(2)(_scale)(ROTATE([1, 2])(PI / 4)(CONE([_width * (1 / SQRT(2)), _height])(4)))


def tetto_triangolo(depth, width):
    """
    Crea un tetto triangolare

    :param width:
    :param depth:
    :return:
    """
    _width = float(width)
    _depth = float(depth)
    return ROTATE([1, 2])(PI / 2)(ROTATE([2, 3])(PI / 2)(
        MULTEXTRUDE(MKPOL([[[0, 0], [_width / 2, _width / 4], [_width, 0]], [[1, 2, 3]], None]))(_depth)))


def lines_to_graph(lines):
    """
    Trasforma un array di linee in un grafo

    :param lines:
    :return:
    """
    keys = {}
    nodes = []
    edges = []

    i = 0

    for line in lines:
        if not (line[0], line[1]) in keys.keys():
            keys[(line[0], line[1])] = i
            nodes.append((line[0], line[1]))
            i = i + 1

        if not (line[2], line[3]) in keys.keys():
            keys[(line[2], line[3])] = i
            nodes.append((line[2], line[3]))
            i = i + 1

        edges.append((keys[(line[0], line[1])], (keys[(line[2], line[3])])))

    return nodes, edges


def tramezzi_centrale():
    """
    Restituisce i tramezzi centrali

    :return:
    """

    def graph_to_tramezzo(g, h):
        return MULTEXTRUDE(OFFSET([40, 40])(STRUCT(MKPOLS(lines_to_graph(g)))))(h)

    centrale = [[4694, 43, 4694, 2000],
                [4694, 2000, 6807, 2000],
                [6807, 2000, 6807, 43],
                [6807, 43, 4694, 43],
                [4694, 43, 4694, 43]]
    centrale_bucato = [[5262, 2000, 4694, 2000],
                       [4694, 2000, 4694, 43],
                       [4694, 43, 6807, 43],
                       [6807, 43, 6807, 2000],
                       [6807, 2000, 6164, 2000]]

    return TOP([
        TOP([
            graph_to_tramezzo(centrale, 400),
            graph_to_tramezzo(centrale_bucato, 700),
        ]),
        graph_to_tramezzo(centrale, 100),
    ])


def tramezzi_laterali():
    """
    Restituisce i tramezzi laterali

    :return:
    """

    def graph_to_tramezzo(g, h):
        return MULTEXTRUDE(OFFSET([40, 40])(STRUCT(MKPOLS(lines_to_graph(g)))))(h)

    tramezzi_laterali = [[4690, 537, 13, 537],
                         [7, 1290, 4687, 1290],
                         [4110, 537, 4110, 1293],
                         [3693, 537, 3693, 1293],
                         [2937, 537, 2937, 1290],
                         [2539, 537, 2539, 1293],
                         [831, 535, 831, 1293],
                         [7, 535, 7, 1803],
                         [11497, 535, 6835, 535],
                         [6841, 1293, 11498, 1293],
                         [7402, 535, 7402, 1293],
                         [8545, 535, 8545, 1293],
                         [9295, 535, 9295, 1293],
                         [9777, 535, 9777, 1293],
                         [10685, 535, 10685, 1293],
                         [11498, 535, 11498, 1752]]

    return graph_to_tramezzo(tramezzi_laterali, 600)


def ripeti(object, times, space=0):
    """
    Funzione che ripete lo stesso oggetto times volte.

    :param object:
    :param times:
    :param space:
    :return:
    """
    moved_object = STRUCT([EMPTY, T(1)(space)(object)])

    def repeat1(object, times, space):
        if (times == 1):
            return moved_object
        else:
            return RIGHT([object, repeat1(moved_object, times - 1, space)])

    return repeat1(object, times, space)


def gorgegous_column(dm, h):
    cylndr = COMP([JOIN, TRUNCONE([dm / 2, .8 * dm / 2, h])])(24)
    torus_bot = COMP([JOIN, TORUS([dm / 2,  .7*dm])])([8, 27])
    base = COMP([T([1, 2])([7 * dm / -12, 7 * dm / -23]), CUBOID])(
        [7 * dm / 6, 7 * dm / 6, dm / 6])
    base_top = COMP([T([1, 2])([7 * dm / -12, 7 * dm / -12]), CUBOID])(
        [7 * dm / 6, 7 * dm / 6, dm / 6])
    capital = SUM([
        COMP([JOIN, TRUNCONE([.8 * dm / 2, 1.2 * dm / 2, h / 8])])(4),
        COMP([R([1, 2])(PI / 4), JOIN, TRUNCONE([.8 * dm / 2, 1.2 * dm / 2, h / 8])])(4)
    ])
    return TOP([TOP([TOP([TOP([base, torus_bot]), cylndr]), capital]), base_top])

def tetto_piccolo():
    return STRUCT([
        tegole()(ROTATE([1,2])(PI/2)(tetto_triangolo(1000, 1300))),
        T(2)(1000)(texture("fronte.jpg")(ROTATE([1, 2])(PI / 2)(tetto_triangolo(1, 1300)))),
    ])

def steps(steps, width, height, depth):
    _steps = float(steps)
    _width = float(width)
    _height = float(height)
    _depth = float(depth)

    def get_step(index):
        s_height = _height/_steps
        s_depth = _depth/_steps
        return T(2)(s_depth*index)(CUBOID([_width, s_depth, (index+1)*s_height]))

    steps = map(get_step, range(0, steps))
    return T([1,2])([6225, 3000])(ROTATE([1,2])(PI)(STRUCT(steps)))


def prato():
    layer1 = T([1, 2, 3])([-1700, -4000, 0])(texture("prato.jpg", 70, 70)(CUBOID([15000, 10000])))
    layer2 = TOP([
        CUBOID([2000, 10000]),
        HEX("#6e6f72")(CUBOID([15000, 2000])),
    ])
    return TOP([layer1, HEX("#b59a5a")(layer2)])

def column(width, height, width_decoration, height_decoration):
    _width = float(width)
    _height = float(height)
    _width_decoration = float(width_decoration)
    _height_decoration = float(height_decoration)
    def get_base():
        translation = -(_width_decoration - _width) / 2
        return T([1, 2])([translation, translation])(CUBOID([_width_decoration, _width_decoration, _height_decoration]))

    return STRUCT([T(3)(_height)(get_base()), CUBOID([_width, _width, _height]), T(3)(0)(get_base())])

def arch(lateral_width, height, deep):

    _lateral_width = float(lateral_width)
    _height = float(height)
    _deep = float(deep)

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

    return Xarc(_lateral_width, _height)(_deep)


def columns():
    columns_12 = ripeti(intonaco()(column(width=100, height=360, width_decoration=130, height_decoration=50)), 12, 300)
    return ripeti(columns_12, 2, 2150)

def archs():
    x = 8
    space = 415
    arch_11 = STRUCT(map(lambda i : T(1)(i*space)(arch(130, 285, 150)), range(0, 11)))
    return intonaco()(ripeti(arch_11, 2, 2140))


def albero(tipologia, rAlbero, hAlbero, hTronco, stagione = SEASON):

    def pattern():
        probability = [.1, .1, .1, .1]
        probability[int(stagione)] = .7
        tipologia = numpy.random.choice(numpy.arange(0, 4), p=probability)
        return str(tipologia)+'.jpg'

    if tipologia == 3:
        tipologia = 2

    hFogliame = hAlbero - hTronco
    if tipologia == 1:
        fogliame = MKPOL([[[0, 0, 0], [0, rAlbero, 0], [0, rAlbero * 1.5 / 4, hFogliame * 1 / 3],
                           [0, rAlbero * 3 / 4, hFogliame * 1 / 3], [0, rAlbero * 1 / 4, hFogliame * 2 / 3],
                           [0, rAlbero * 2 / 4, hFogliame * 2 / 3],
                           [0, 0, hFogliame], [0, 0, hFogliame * 2 / 3], [0, 0, hFogliame * 1 / 3]],
                         [[1, 2, 3, 9], [9, 4, 5, 8], [8, 6, 7]], 1])
        fogliame = texture(pattern())(fogliame)
        c1 = texture(pattern())(CYLINDER([rAlbero * 1 / 2, 0])(10))
        c2 = texture(pattern())(CYLINDER([rAlbero * 3 / 8, 0])(10))
        c3 = texture(pattern())(CYLINDER([rAlbero * 2 / 8, 0])(10))
        fogliame = STRUCT([fogliame, c1, T(3)(hFogliame * 1 / 3), c2, T(3)(hFogliame * 1 / 3), c3])

    elif tipologia == 2:
        fogliame = T(3)(rAlbero * 1 / 2)(R([1, 3])(math.pi / 2)(CYLINDER([rAlbero * 1 / 2, 0])(20)))
        fogliame = S([2, 3])([2, hFogliame / rAlbero])(fogliame)
        fogliame = texture(pattern())(fogliame)
        c1 = texture(pattern())(CYLINDER([rAlbero * 1 / 2, 0])(10))
        c2 = texture(pattern())(CYLINDER([rAlbero * 5 / 6, 0])(10))
        c3 = texture(pattern())(CYLINDER([rAlbero * 1 / 2, 0])(10))
        fogliame = STRUCT(
            [fogliame, T(3)(hFogliame * 1 / 4), c1, T(3)(hFogliame * 1 / 4), c2, T(3)(hFogliame * 1 / 4),
             c3])

    fogliame = STRUCT([fogliame, S(2)(-1), fogliame])
    i = 0
    while i < 3.14:
        i += 3.14 / 4
        fogliame = STRUCT([fogliame, R([1, 2])(i), fogliame])

    trunk = MATERIAL([
        0.0, 0.0, 0.0, 1.0, 0.459, 0.27157, 0.0000, 1, 0.0225, 0.0225, 0.0225, 1.0, 0.0, 0.0, 0.0, 1.0,12.8
    ])(CYLINDER([rAlbero / 16, hTronco])(10))
    tree = STRUCT([trunk, T(3)(hTronco), fogliame])

    return tree

tramezzi_centrale = intonaco()(tramezzi_centrale())
tramezzi_laterali = intonaco()(tramezzi_laterali())
tetto_centrale = tegole()(tetto_piramidale(2000, 2150, 400))
tetti_laterali = tegole(6, 6)(ripeti(tetto_triangolo(4700, 1300), 2, 2150))
gorgeous_columns = intonaco()(ripeti(gorgegous_column(100., 580.), 4, 220))
scale = LEFT([
    RIGHT([
        texture("steps.jpg", 2, 2)(steps(25, 920, 400, 1000)),
        texture("1.jpg", 2, 2)(steps(25, 50, 500, 1000))
    ]),
    texture("1.jpg", 2, 2)(steps(25, 50, 500, 1000))
])
floor = texture("atrio.jpg")(T([1, 2, 3])([4700, 50, 400])(CUBOID([2150, 1950, 1])))

def foresta(stagione=0):
    def get_random_tree():
        tipologia = random.randint(1,3)
        rAlbero = float(300)
        rAlbero = float(300)
        hAlbero = float(random.randint(400, 800))
        hTronco = hAlbero/4
        return albero(tipologia,rAlbero,hAlbero,hTronco)

    return STRUCT([
        STRUCT(map(lambda x: T([1, 2])([random.randint(-1000,4500), random.randint(2500,5500)])(get_random_tree()), range(0, 50))),
        T(1)(8500)(STRUCT(map(lambda x: T([1, 2])([random.randint(-1000,4500), random.randint(2500,5500)])(get_random_tree()), range(0, 50)))),
        T([1,2])([8500,-6000])(STRUCT(map(lambda x: T([1, 2])([random.randint(-1000, 4500), random.randint(2500, 5500)])(get_random_tree()), range(0, 50)))),
        T([1, 2])([0, -6000])(STRUCT(map(lambda x: T([1, 2])([random.randint(-1000, 4500), random.randint(2500, 5500)])(get_random_tree()), range(0, 50)))),
    ])

def torre():
    l = 700
    return TOP([
        intonaco()(CUBOID([l, l, 1200])),
        tegole()(tetto_piramidale(l, l, 200))
    ])

VIEW(
    STRUCT([
        MIDDLE([
            MIDDLE([
                MIDDLE([
                    TOP([tramezzi_centrale, tetto_centrale]),
                    STRUCT([EMPTY, T([2, 3])([1000, 1200])(tetto_piccolo())]),
                ]),
                STRUCT([EMPTY, T([2, 3])([2000, 400])(gorgeous_columns)]),
            ]),
            STRUCT([EMPTY, T(2)(1400)(TOP([columns(), archs()]))]),
        ]),
        TOP([tramezzi_laterali, tetti_laterali]),
        scale,
        floor,
        prato(),
        foresta(1),
        T(2)(535)(ripeti(torre(), 2, 10147)),
    ]),
)
