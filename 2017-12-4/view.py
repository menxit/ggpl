from larlib import *

r0 = 24.
r2 = 48.
r3 = 72.
r4 = 88.
wsteps = 10.
nsteps = 10.
wstep = wsteps / nsteps
hstep = 1. / 3.
hw4 = 29.
hbasament = hstep * nsteps


# Mappa cilindrica
def cylMap(dev=True):
    if dev:
        return MAP([lambda p: (p[1]) * math.cos(p[0]), lambda p: (p[1]) * math.sin(p[0]), lambda p: (p[2])])
    else:
        return MAP([lambda p: (p[1]) * math.sin(p[0]), lambda p: (p[1]) * math.cos(p[0]), lambda p: (p[2])])


# Scala esterna
def vdom(h):
    return PROD([
        COMP([
            EMBED(1),
            INTERVALS(PI * 3 / 24)
        ])(3),
        QUOTE([h])
    ])


def hdom(w):
    return COMP([S(2)(-1), EMBED(1)])(PROD([INTERVALS(PI * 3 / 24)(3), QUOTE([w])]))


def steps(w, h):
    def steps1(n):
        return COMP([STRUCT, CAT, N(n)])([vdom(h), T(3)(h), hdom(w), T(2)(-w)])

    return steps1


hbasament = hstep * nsteps

stair = RIGHT([
    COMP([MKPOL, UKPOL])(steps(wstep, hstep)(nsteps)),
    COMP([S(2)(-1), SKEL_2, CUBOID])([PI / 24, wsteps, hbasament])
])
ramp = cylMap()(T(2)(r4)(stair))
stairs = STRUCT(NN(12)([ramp, R([1, 2])(PI / 6)]))

# Basamento
basisSector = COMP([cylMap(False), EMBED(1)])(
    PROD([INTERVALS(2 * PI / 12)(4), INTERVALS(r4 - (wstep * (nsteps - 1)))(1)]))
basis = COMP([STRUCT, NN(12)])([basisSector, R([1, 2])(2 * PI / 12)])
basement = COMP([R([1, 2])(PI / -48), STRUCT])([stairs, T(3)(hstep * nsteps), basis])

# Muro esterno
ExtWall2Da = INTERSECTION([
    MKPOL([[[0, 0], [7, 0], [7, 5], [0, 8], [7, 3], [9, 4], [10.5, 1.5], [10.5, 0], [11, 1.5], [11, 3]],
           [range(1, 5), [2, 8, 7, 6, 5], [6, 7, 9, 10]], [[1], [2], [3]]]),
    PROD([COMP([QUOTE, N(12)])(1), Q(8)])
])

ExtWall2Db = INTERSECTION([
    MKPOL([[[0.5, 0], [4, 0], [5, 0], [6, 0], [6, 3], [5.5, 3.5], [5, 3], [4.5, 3.5], [4, 3], [2, 4], [0, 3], [0, 1.5],
            [0.5, 1.5]], [[10, 11, 12, 13], [1, 2, 9, 10, 13], [2, 3, 7, 8, 9], [3, 4, 5, 6, 7]], range(1, 5)]),
    PROD([COMP([QUOTE, N(6)])(1), Q(4)])
])

ExtWall2D = STRUCT([ExtWall2Da, T(1)(11), ExtWall2Db])

sizxExtWall = SIZE(1)(ExtWall2D)

ExtWall = R([2, 3])(PI / 2)(PROD([ExtWall2D, QUOTE([1.5])]))

CurvedExtWall = COMP([cylMap(False), T(2)(r3), S([1, 3])([PI / (4 * sizxExtWall), hw4 / 8])])(ExtWall)

DoubleExtWall = STRUCT([CurvedExtWall, S(1)(-1), CurvedExtWall])

FullExtWall = COMP([STRUCT, NN(4)])([DoubleExtWall, R([1, 2])(PI / 2)])

# Colonne intermedie
hCol = 12.


def Column(args):
    w, h = args
    basis = CUBOID([w, w, 2. * w / 3.])
    trunk = CYLINDER([w / 2. * .85, h - w])(8)
    capitel = CUBOID([w, w, w / 3.])
    return TOP([TOP([basis, trunk]), capitel])


arcAngle = 2. * PI / 50.4
wallAngle = -3.2 * arcAngle / 4.
RotCross = 3.2 * arcAngle / 4. + 2.5 * arcAngle

MyColumn = COMP([MKPOL, UKPOL, T(2)(r2 - .75), Column])([1.5, hCol])

The4cols = COMP([R([1, 2])(arcAngle * .4 / 3.2), MKPOL, UKPOL, STRUCT, NN(4)])([R([1, 2])(DIFF(arcAngle)), MyColumn])

The5Cols = COMP([R([1, 2])(arcAngle * .4 / 3.2), MKPOL, UKPOL, STRUCT, NN(5)])([R([1, 2])(DIFF(arcAngle)), MyColumn])

TheBotWal = COMP([cylMap(False), MKPOL, UKPOL, T(2)(r2 - .75), CUBOID])([3.2 * arcAngle / 4, 1.5, hCol])

TheSecCols = STRUCT([
    R([1, 2])(RotCross),
    TheBotWal, R([1, 2])(wallAngle),
    The4cols, R([1, 2])(-5 * arcAngle),
    TheBotWal, R([1, 2])(wallAngle),
    The5Cols
])

TheMedColumns = COMP([STRUCT, NN(4)])([TheSecCols, R([1, 2])(PI / -2.)])


# Archi sulle colonne

def bottomArc(d):
    return BEZIER(S1)([[0, 0], [0, 2 * d / 3], [d, 2 * d / 3], [d, 0]])


def topArc(d):
    return BEZIER(S1)([[0, 2 * d / 3], [d, 2 * d / 3]])


def arc2D(d):
    return BEZIER(S2)([bottomArc(d), topArc(d)])


def arc3D(d):
    def arc3D1(w):
        arco = arc2D(3.2)
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


TheArc = Xarc(0.4, 3.2)(1.5)
SizeArc = SIZE(1)(TheArc)
sx = (1 / SizeArc) * arcAngle
sz = sx * (r2 - 2)

CurvedArc = COMP([cylMap(False), MKPOL, UKPOL, T(2)(r2 - .75), S([1, 3])([sx, sz])])(TheArc)
HeigthArc = SIZE(3)(CurvedArc)

The5arcs = COMP([MKPOL, UKPOL, STRUCT, NN(5)])([CurvedArc, R([1, 2])(-arcAngle)])
The6arcs = COMP([MKPOL, UKPOL, STRUCT, NN(6)])([CurvedArc, R([1, 2])(-arcAngle)])
TheMidWall = COMP([cylMap(False), MKPOL, UKPOL, T(2)(r2 - .75), CUBOID])([3.2 * arcAngle / 4, 1.5, HeigthArc])
TheSector = STRUCT(
    [R([1, 2])(RotCross), TheMidWall, R([1, 2])(wallAngle), The5arcs, R([1, 2])(-5 * arcAngle), TheMidWall,
     R([1, 2])(wallAngle), The6arcs])
TheArcs = COMP([STRUCT, NN(4)])([TheSector, R([1, 2])(PI / -2)])
TheArcsCols = STRUCT([TheMedColumns, T(3)(hCol), TheArcs])

# Muro intermedio superiore
MedWall2D = INTERSECTION([MKPOL(
    [[[0, 4], [8, 4], [17, 4], [17, 5], [12.5, 7.5], [8, 5], [0, 8]], [[1, 2, 6, 7], [2, 3, 4, 5, 6]], [[1], [2]]]),
    PROD([COMP([QUOTE, N(17)])(1), QUOTE([8])])])
sizxMedWall = SIZE(1)(MedWall2D)
MedWall = R([2, 3])(PI / 2)(PROD([MedWall2D, QUOTE([1.5])]))
CurvedMedWall = COMP([cylMap(), MKPOL, UKPOL, T(2)(r2 + 0.75), S([1, 3])([PI / (4 * sizxMedWall), hw4 / 8])])(MedWall)
DoubleMedWall = STRUCT([CurvedMedWall, S(1)(-1)(CurvedMedWall)])
FullMedWall = COMP([STRUCT, NN(4)])([DoubleMedWall, R([1, 2])(PI / 2)])
MedWallArcs = STRUCT([FullMedWall, TheArcsCols])

# Muri laterali della croce
CrossWall = COMP([T(1)(-1), R([1, 2])(0.2 * arcAngle), S(3)(hw4 / 8), CUBOID])([1.5, r3 - r2, 5])
SingleWall = COMP([R([1, 2])(2.5 * arcAngle), T(2)(r2)])(CrossWall)
DoubleWall = STRUCT([SingleWall, S(1)(-1), SingleWall])
CrossWalls = COMP([STRUCT, NN(4)])([DoubleWall, R([1, 2])(PI / 2)])

# Tetto sulla croce
HalfTetto = MKPOL([[[0, r2, 8], [8, r2, 5], [8, r3, 5], [0, r3, 8]], [[1, 2, 3, 4]], []])
CurvedHalfTetto = COMP([cylMap(), S([1, 3])([2.5 * arcAngle / 8, hw4 / 8])])(HalfTetto)
DoubleHalfTetto = STRUCT([CurvedHalfTetto, S(1)(-1)(CurvedHalfTetto)])
FullTetto = COMP([STRUCT, NN(4)])([DoubleHalfTetto, R([1, 2])(PI / -2)])


# Muro con Triplice apertura
def CourtWall(d1, d2):
    def CourtWall1(n1, n2):
        w = 0.7
        TripleHole = TOP([STRUCT([Column([w, 2]), T(1)(2 + w), Column([w, 2])]), Xarc(2, 2)(1)])
        h = SIZE(3)(TripleHole)
        op = ALIGN([[1, MAX, MIN], [2, MIN, MIN]])
        LeftWall = PROD([COMP([QUOTE, N(n1)])(d1 / n1), CUBOID([1, h])])
        RightWall = PROD([COMP([QUOTE, N(n2)])(d2 / n2), CUBOID([1, h])])
        return op([op([LeftWall, TripleHole]), RightWall])

    return CourtWall1


# Muro inferiore Cortile interno
MyCourtWall = CourtWall(12, 12)(9, 9)
sizxCourtWall = SIZE(1)(MyCourtWall)
mapping = COMP([cylMap(False), S([1, 3])([(7.25 * PI / 24) * (1 / sizxCourtWall), hw4 / 8])])
CurvedCourtWall = COMP([OPTIMIZE, R([1, 2])(-2.5 * arcAngle), mapping, T(2)((r3 + r2) / 2)])(MyCourtWall)
CrossCourtWall = COMP([STRUCT, NN(4)])([CurvedCourtWall, R([1, 2])(PI / 2)])

# Coronamento Muro Cortile interno
TopCourtWall2D = INTERSECTION(
    [MKPOL([[[0, 3.333], [10, 3.333], [10, 4.333], [5, 6.333], [0, 4.333]], [range(1, 5)], [[1]]]),
     PROD([COMP([QUOTE, N(10)])(1), QUOTE([8])])])
TopCourtWall = R([2, 3])(PI / 2)(PROD([TopCourtWall2D, QUOTE([1])]))
MyTopCourtWall = RIGHT([TopCourtWall, RIGHT([TopCourtWall, TopCourtWall])])
CurvedTopCourtWall = COMP([R([1, 2])(-2.5 * arcAngle), mapping, T(2)((r3 + r2 + 2) / 2)])(MyTopCourtWall)
FullTopCourtWall = COMP([STRUCT, NN(4)])([CurvedTopCourtWall, R([1, 2])(PI / 2)])

# Tetto su Cortile interno
RotWall = 2.5 * arcAngle
CourTetto = INTERSECTION([MKPOL([[[0, (r3 + r2 + 2) / 2, 3.333], [10, (r3 + r2 + 2) / 2, 3.333], [10, r2, 4.333],
                                  [0, r2, 4.333], [0, (r3 + r2 + 2) / 2, 3.433], [10, (r3 + r2 + 2) / 2, 3.433],
                                  [10, r2, 4.433], [0, r2, 4.433]], [range(1, 9)], [[1]]]),
                          PROD([COMP([QUOTE, N(10)])(1), PROD([QUOTE([(r3 + r2 + 2) / 2]), QUOTE([5])])])])

MyCourTetto = RIGHT([RIGHT([CourTetto, CourTetto]), CourTetto])
CurvedCourTetto = COMP([R([1, 2])(DIFF(RotWall)), mapping])(MyCourTetto)
FullCourTetto = COMP([STRUCT, NN(4)])([CurvedCourTetto, R([1, 2])(PI / 2)])


# Colonne muro interno
def Radial22Obj(Obj):
    The4Obj = COMP([STRUCT, NN(4)])([Obj, R([1, 2])(PI / 11)])
    The2Obj = COMP([STRUCT, NN(2)])([Obj, R([1, 2])(PI / 11)])
    The20Obj = COMP([STRUCT, NN(5)])([The4Obj, R([1, 2])((4 * PI) / 11)])
    return STRUCT([The20Obj, R([1, 2])((20 * PI) / 11), The2Obj])


InternalCol = COMP([MKPOL, UKPOL, T(2)((r0 - 2)), Column])([1.5, hCol])
The22Columns = Radial22Obj(InternalCol)

# Travi muro interno
Beam = PROD([QUOTE([-0.5, 1.5, 2, 1.5]), PROD([QUOTE([2.2]), QUOTE([1.5])])])
CurvedBeam = COMP([cylMap(), T([2, 3])([(r0 - 2), hCol]), S(1)(PI / (11 * 5))])(Beam)
The22Beams = Radial22Obj(CurvedBeam)

# Muro interno superiore
Hwall = STRUCT([
    INSR(PROD)([QUOTE([-0.5, 1.5, -2, 1.5]), QUOTE([-0.3, 1.4]), QUOTE([2.5 * hCol])]),
    INSR(PROD)([QUOTE([-2.0, 2]), QUOTE([-0.3, 1.4]), QUOTE([1.5 * hCol, -0.5 * hCol, 0.5 * hCol])]),
    INSR(PROD)([QUOTE([-2.25, 1.5]), QUOTE([-0.3, 1.4]), QUOTE([1.5 * hCol, -0.5 * hCol, 0.5 * hCol])])
])

CurvedHwall = COMP([cylMap(False), T([2, 3])([r0 - 2, hCol]), S(1)(PI / (11 * 5))])(Hwall)

The22Hwall = Radial22Obj(CurvedHwall)

# Coronamento superiore muro interno
myArc = MAP([COMP([SIN, S1]), COMP([COS, S1])])(QUOTE(N(5)(PI / 10)))
Vertex = MKPOL([[[0, 0]], [[1]], [[1]]])
Sector = JOIN([myArc, Vertex])
Triangle = S(1)(-1)(SIMPLEX(2))
SectorTriangle2D = STRUCT([T(1)(0.05), Sector, T(1)(2), Triangle])
DoubleSect = STRUCT([SectorTriangle2D, S(1)(-1)(SectorTriangle2D)])
Sect2D = S(1)(2 / 2.05)(DoubleSect)
Sect3D = R([2, 3])(PI / 2)(PROD([Sect2D, QUOTE([0.8])]))
CurvedSect = COMP([cylMap(False), T(2)(r0), S([1, 3])([(2 * PI) / (11 * 4), 3])])(Sect3D)
Frieze = T(3)(3.5 * hCol)(CurvedSect)


def Radial11Obj(Obj):
    The2Obj = COMP([STRUCT, NN(2)])([Obj, R([1, 2])((2 * PI) / 11)])
    The10Obj = COMP([STRUCT, NN(5)])([The2Obj, R([1, 2])((4 * PI) / 11)])
    return STRUCT([The10Obj, R([1, 2])((20 * PI) / 11), Obj])


The11Frieze = Radial11Obj(Frieze)


# Traliccio Tetto interno
def Trellis(v):
    H, L = v
    return COMP([R([2, 3])(PI / 2.), EMBED(1), MKPOL])(
        [[[0, 0], [L / 3, 0], [2 * L / 3, 0], [L, 0], [2 * L / 3, H / 3], [L / 3, 2 * H / 3], [0, H]],
         [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 1], [1, 6], [6, 2], [2, 5], [5, 3]],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]])


def Radial(n):
    def Radial1(obj):
        return COMP([STRUCT, NN(3)])([
            COMP([STRUCT, NN(n / 3)])([obj, R([1, 2])(2 * PI / n)]),
            R([1, 2])(2 * PI / 3)
        ])

    return Radial1


TrellisTop3D = COMP([T(2)(-.25), S(2)(.5), OFFSET([1, 1, 1]), Trellis])([hCol, r0 - 1])

TheTopTrellis = T(3)(3.5 * hCol)(TrellisTop3D)

TopTrellis = Radial(12)(TheTopTrellis)

# Traliccio Tetto intermedio
TrellisMed3D = COMP([T(2)(-0.25), S(2)(0.5), OFFSET([1, 1, 1]), Trellis])([hCol, r2 - r0])
TheMedTrellis = T(3)(hCol + 3)(TrellisMed3D)
MedTrellis = Radial(24)(T(1)(r0)(TheMedTrellis))
DoubleMedTrellis = STRUCT([MedTrellis, R([1, 2])(PI / 24), MedTrellis])

VIEW(STRUCT([basement, T(3)(hbasament), FullExtWall, FullTetto, CrossCourtWall, CrossWalls, MedWallArcs, TheMedColumns,
             FullTopCourtWall, FullCourTetto, The22Columns, The22Beams, The22Hwall, The11Frieze, TopTrellis,
             DoubleMedTrellis]))
