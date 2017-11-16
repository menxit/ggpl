from pyplasm import VIEW, STRUCT
from lib.utilities import arrangedCircularly
from lib.abstractStructure import abstractStructure
from lib.columna import columna

VIEW(STRUCT([
    arrangedCircularly(abstractStructure(16, True), 70, 10),
    arrangedCircularly(columna(6, 25), 100, 10),
    abstractStructure(16, False)
]))

quit()
