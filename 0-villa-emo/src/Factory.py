from Planimetry import *
from Steps import *
from VillaEmo import *
from Column import *
from Triangle import *
from Brecciolino import *

def create_planimetry():
    assets = [
        {'file': '../assets/centrale.lines', 'height': 50},
        {'file': '../assets/laterale.lines', 'height': 30}
    ]
    return Planimetry(assets)


def create_steps():
    return Steps(steps=10, width=92, height=5, depth=50)


def create_villa_emo():
    return VillaEmo()


def create_column():
    return Column(width=10, height=29, width_decoration=13, height_decoration=5)

def create_brecciolino():
    assets = [
        {'file': '../assets/brecciolino.lines'},
    ]
    return Brecciolino(assets)
