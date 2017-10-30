from pyplasm import T, MATERIAL, CUBOID, STRUCT, HEX, DIFFERENCE


def hex_material(color, light, trasparence):
    """
    Edits the color and trasparency of the object.
    :param color:
    :param light:
    :param trasparence:
    :return:
    """
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return map(lambda x: x/255., list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))

    # ambientRGBA, diffuseRGBA specularRGBA emissionRGBA shininess
    params = hex_to_rgb(color) + [.1] + \
             hex_to_rgb(light) + [trasparence] +\
             hex_to_rgb(light) + [.1] +\
             hex_to_rgb("#000000") + [.1] +\
             [100]

    return MATERIAL(params)


def armadio(
    larghezza_armadio,
    altezza_armadio,
    profondita_armadio,
    spessore_cornice,
    numero_ante,
    numero_ripiani,
    color
):
    """
    permette di creare un armadio parametrizzato.
    :param larghezza_armadio:
    :param altezza_armadio:
    :param profondita_armadio:
    :param numero_ante:
    :param numero_ripiani:
    :param color:
    :param spessore_cornice:
    :return:
    """
    def anta(larghezza_anta):
        """
        crea un'anta
        :param larghezza_anta:
        :return:
        """
        cornice = CUBOID([larghezza_anta, altezza_armadio, spessore_cornice])
        vetro = T([1, 2])([spessore_cornice, spessore_cornice])(
            CUBOID([larghezza_anta - spessore_cornice * 2, altezza_armadio - spessore_cornice * 2, spessore_cornice]))
        vetro = hex_material("#00EAFF", "#00EAFF", .4)(vetro)
        cornice = HEX(color)(DIFFERENCE([cornice, vetro]))

        return STRUCT([cornice, vetro])

    def ante(N):
        """
        genera N ante dell'armadio
        :param N:
        :return:
        """
        if(N == 0):
            return CUBOID([0])
        return STRUCT(map(lambda i: T([1, 3])([float(larghezza_armadio)/N*i, profondita_armadio])(
            anta(float(larghezza_armadio)/N)), range(0, N)))

    def ripiani(N):
        """
        genera N ripiani dell'armadio
        :param N:
        :return:
        """
        if (N == 0):
            return CUBOID([0])
        return STRUCT(map(lambda i: T([1, 2])([spessore_cornice, (float(altezza_armadio)/(N+1))*(i+1)])(ripiano()), range(0, N)))

    def ripiano():
        return HEX(color)(CUBOID([larghezza_armadio - (spessore_cornice * 2), spessore_cornice, profondita_armadio]))

    def struttura():
        return HEX(color)(DIFFERENCE([
            CUBOID([larghezza_armadio, altezza_armadio, profondita_armadio]),
            T([1, 2, 3])([spessore_cornice, spessore_cornice, spessore_cornice])(CUBOID([
                larghezza_armadio-(spessore_cornice*2),
                altezza_armadio-(spessore_cornice*2),
                profondita_armadio
            ]))
        ]))

    return STRUCT([
        ante(numero_ante),
        ripiani(numero_ripiani),
        struttura()
    ])


def composizione_armadio():
    armadio1 = T([1, 2, 3])([0, 0, 0])(armadio(
        larghezza_armadio=1.2,
        altezza_armadio=2.8,
        profondita_armadio=1.2,
        spessore_cornice=.03,
        numero_ante=0,
        numero_ripiani=6,
        color="#2c3e50",
    ))

    armadio2 = T([1, 2, 3])([1.2, 1.6, 0])(armadio(
        larghezza_armadio=2,
        altezza_armadio=1.2,
        profondita_armadio=.7,
        spessore_cornice=.03,
        numero_ante=4,
        numero_ripiani=2,
        color="#34495e",
    ))

    armadio3 = T([1, 2, 3])([3.2, 1.6, 0])(armadio(
        larghezza_armadio=1,
        altezza_armadio=.6,
        profondita_armadio=.7,
        spessore_cornice=.03,
        numero_ante=0,
        numero_ripiani=0,
        color="#2c3e50",
    ))

    pavimento = HEX("#c0392b")(CUBOID([6, 0, 4]))

    parete = HEX("#c0392b")(CUBOID([6, 3.5]))

    return STRUCT([parete, pavimento, T(1)(1)(STRUCT([armadio1, armadio2, armadio3]))])
