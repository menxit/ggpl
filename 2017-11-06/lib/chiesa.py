from pyplasm import *

C1 = "#EBE5D9"
C2 = "#747474"


def HEMISPHERE(radius):
    """
    Hemisphere
    :param radius:
    :return:
    """
    def HEMISPHERE1 (subds):
        N , M = subds
        domain = Plasm.translate( Plasm.power(INTERVALS(PI/2)(N) , INTERVALS(2*PI)(M)), Vecf(0, -PI/2,0 ) )
        fx  = lambda p: radius * math.cos(p[0])  * math.sin  (p[1])
        fy  = lambda p: radius * math.cos(p[0]) * math.cos (p[1])
        fz  = lambda p: radius * math.sin(p[0])
        ret=  MAP([fx, fy, fz])(domain)
        return ret
    return HEMISPHERE1

def chiesa(diametro, altezza, N = 8):
    """
    Restituisce un oggetto PyPlasm rappresentate una chiesa basata su disegni di Leonardo Da Vinci.
    :param diametro:
    :param altezza:
    :param N:
    :return:
    """
    def base():
        return HEX(C1)(STRUCT([
            CYLINDER([diametro, .25])(60),
            T(3)(.25)(CYLINDER([diametro - .5, .25])(60)),
            T(3)(.5)(CYLINDER([diametro - 1, .25])(60)),
        ]))

    def corpus():
        return HEX(C2)(
            DIFFERENCE([
                CYLINDER([diametro - 1.5, altezza])(60),
                CYLINDER([diametro - 1.5 - diametro/2, altezza + 1])(60),
                disponi_circolarmente(T(3)(1)(CYLINDER([diametro / 4, altezza])(60)), -1),
                disponi_circolarmente(T(3)(1)(CYLINDER([diametro / 4, altezza/2])(60)), diametro, 16),
            ])
        )

    def colonne_esterne():
        c = STRUCT([
            DIFFERENCE([
                T(3)(altezza)(CYLINDER([diametro / 4, altezza/5])(60)),
                T(3)(altezza)(CYLINDER([diametro / 4 - 1, altezza/5])(60)),
            ]),
            T(3)(altezza+altezza/5)(R([1,3])(-PI)(HEMISPHERE(diametro / 4)([8, 8])))
        ])
        return disponi_circolarmente(c)

    def disponi_circolarmente(object, aggiungi_raggio = 0, N = N):
        r = diametro-diametro/4-1.5-1 + aggiungi_raggio
        colors = [C1, C2]
        return STRUCT(map(lambda i: T([1, 2])([r*math.cos((2*PI/N)*i), r*math.sin((2*PI/N)*i)])(HEX(colors[i%2])(R([1,2])((2*PI/(N))*i)(object))), range(0, N)))

    def cuppolone():
        return STRUCT([
            HEX(C1)(DIFFERENCE([
                T(3)(altezza)(CYLINDER([diametro / 2, altezza/1.5])(60)),
                T(3)(altezza)(CYLINDER([diametro / 2 - 1, altezza/1.5])(60)),
            ])),
            HEX(C2)(T(3)(altezza+altezza/1.5)(R([1,3])(-PI)(HEMISPHERE(diametro / 2)([8, 8]))))
        ])

    def puntale():
        return HEX(C1)(T(3)(altezza + diametro)(STRUCT([
            CYLINDER([2, 2])(60),
            CYLINDER([1.5, 4])(60),
            CYLINDER([.8, 5])(60),
            CYLINDER([.4, 6])(60),
            T(3)(6)(R([1,3])(-PI)(HEMISPHERE(.4)([8, 8])))
        ])))


    def details():
        return CYLINDER([.4, 6])(60),

    def render():
        return STRUCT([
            base(),
            corpus(),
            colonne_esterne(),
            cuppolone(),
            puntale(),
        ])

    return render()
