# pacman.py
# author: Elhex
#
# Description: Logic and behavior of PacMan (movement, input, score)

from ursina import *
from constants import EAT_PELLET_SCORE, EAT_POWER_PELLET_SCORE


class PacMan(Entity):
    def __init__(self, position, game, **kwargs):
        self.game = game
        super().__init__(position=position, **kwargs)
        self.model = 'sphere'
        self.color = color.yellow
        self.scale = 1.8
        self.speed = 5
        self.collider = 'box'

       
        self._score = 0

        self.direction = Vec3(0, 0, 0)
        self.next_direction = Vec3(0, 0, 0)

    @property 
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if value < 0:
            value = 0
        self._score = value

    def update(self):
        #stop movement if transition is in progress
        if self.game.transition_in_progress:
            return
        self.process_input()
        self.move()

    def process_input(self):
        move_dir = Vec3(0, 0, 0)
        if held_keys['w']:
            move_dir.y += 1
        if held_keys['s']:
            move_dir.y -= 1
        if held_keys['a']:
            move_dir.x -= 1
        if held_keys['d']:
            move_dir.x += 1

        if move_dir.length() > 0:
            self.next_direction = move_dir.normalized()

    def move(self):
        """pacman movement logic"""
        new_pos = self.position + self.direction * self.speed * time.dt
        if not self.game.colliding_with_wall_2d(new_pos, self.scale / 2):
            self.position = new_pos
        else:
            self.direction = Vec3(0, 0, 0)

        check_pos = self.position + self.next_direction * self.speed * time.dt
        if not self.game.colliding_with_wall_2d(check_pos, self.scale / 2):
            self.direction = self.next_direction

