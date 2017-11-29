import os
from utilities import *
from larlib import *

def villaEmo():
    scriptDir = os.path.dirname(__file__)

    nodiLaterali, archiLaterali = linesToGraph(os.path.join(scriptDir, "../assets/laterale.lines"))
    nodiCentrale, archiCentrale = linesToGraph(os.path.join(scriptDir, "../assets/centrale.lines"))

    piantaLaterale = MULTEXTRUDE(OFFSET([2, 2])(STRUCT(MKPOLS((nodiLaterali, archiLaterali)))))(30)
    piantaCentrale = MULTEXTRUDE(OFFSET([2, 2])(STRUCT(MKPOLS((nodiCentrale, archiCentrale)))))(50)

    return STRUCT([piantaLaterale, piantaCentrale])
