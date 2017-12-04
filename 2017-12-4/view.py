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
cylMap = MAP([lambda p: (p[1]) * math.cos(p[0]), lambda p: (p[1]) * math.sin(p[0]), lambda p: (p[2])])


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
ramp = cylMap(T(2)(r4)(stair))
stairs = STRUCT(NN(12)([ramp, R([1, 2])(PI / 6)]))

# Basamento
basisSector = COMP([cylMap, EMBED(1)])(PROD([INTERVALS(2 * PI / 12)(4), INTERVALS(r4 - (wstep * (nsteps - 1)))(1)]))
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

CurvedExtWall = COMP([cylMap, T(2)(r3), S([1, 3])([PI / (4 * sizxExtWall), hw4 / 8])])(ExtWall)

DoubleExtWall = STRUCT([CurvedExtWall, S(1)(-1), CurvedExtWall])

FullExtWall = COMP([STRUCT, NN(4)])([DoubleExtWall, R([1, 2])(PI / 2)])

# Colonne intermedie


"""


DEF The5cols = (R:<1,2>:(arcAngle*0.4/3.2) ~ MKPOL ~ UKPOL ~ 
  STRUCT ~ ##:5):< R:<1,2>:(-:arcAngle), MyColumn >;
DEF TheBotWal = (cylMap ~ MKPOL ~ UKPOL ~ T:2:(r2 - 0.75) ~ CUBOID):
  < 3.2*arcAngle/4, 1.5, hCol >;
DEF TheSecCols = STRUCT:< R:<1,2>:RotCross,
  TheBotWal, R:<1,2>:wallAngle, 
  The4cols, R:<1,2>:(-5*arcAngle), 
  TheBotWal, R:<1,2>:wallAngle, 
  The5cols >;
"""
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

TheBotWal = COMP([cylMap, MKPOL, UKPOL, T(2)(r2 - .75), CUBOID])([3.2 * arcAngle / 4, 1.5, hCol])

TheSecCols = STRUCT([
    R([1, 2])(RotCross),
    TheBotWal, R([1, 2])(wallAngle),
    The4cols, R([1, 2])(-5 * arcAngle),
    TheBotWal, R([1, 2])(wallAngle),
    The5Cols
])

TheMedColumns = COMP([STRUCT, NN(4)])([TheSecCols, R([1, 2])(PI / -2.)])

VIEW(STRUCT([basement, T(3)(hbasament), FullExtWall, TheMedColumns]))
