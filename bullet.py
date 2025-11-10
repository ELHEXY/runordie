# bullet.py
# author: Elhex
#
# Description: Bullet class for the game (2D/3D)
#      
#--------------------------------------------------------------------------------------

from ursina import *
import math
from constants import BULLET_LIFETIME, BULLET_COLLISION_DISTANCE_3D

class Bullet(Entity):
    def __init__(self, position, direction, game, speed=20, **kwargs):
        self.game = game
        super().__init__(position=position, **kwargs)
        self.model = 'sphere'
        self.scale = 0.1
        self.color = color.red
        self.direction = direction.normalized()
        self.speed = speed
        self.life_time = BULLET_LIFETIME
        self.collider = 'sphere'

    def update(self):
        # stop movement if transition is in progress
        if self.game.transition_in_progress:
            return

        self.position += self.direction * self.speed * time.dt
        self.life_time -= time.dt
        if self.life_time <= 0:
            self.disable()  
            return

        # check collision with ghosts
        for ghost in self.game.ghosts_3d:
            if ghost and ghost.enabled and distance(self.position, ghost.position) < BULLET_COLLISION_DISTANCE_3D:
                ghost.take_damage(5)
                self.disable()
                break
