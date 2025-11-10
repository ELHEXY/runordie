# pellets.py
# author: Elhex
#
# Description: Pellets and PowerPellets classes for PacMan game
#
from ursina import *


class Pellet(Entity):
    def __init__(self, position):
        super().__init__()
        self.model = 'sphere'
        self.color = color.white
        self.position = position
        self.scale = 0.4
        self.collider = None

class PowerPellet(Pellet):
    def __init__(self, position):
        super().__init__(position)
        self.scale = 0.7
        self.color = color.white
