# ghost.py
# author: Elhex
#
# Description: Logic and behavior of the ghosts for 2D/3D modes

from ursina import *
import math, random, time
from constants import (
    GHOST_ALERT_DISTANCE_2D, GHOST_ALERT_DISTANCE_3D,
    GHOST_CHANGE_DIRECTION_INTERVAL, GHOST_MAX_HEALTH,
    GHOST_SCALE_2D, GHOST_SCALE_3D
)

class Ghost(Entity):
    """
    Ghost class represents a ghost in the game. It can be in 2D or 3D mode.
    """
    def __init__(self, position, mode='2d', game=None, ghost_color=None, **kwargs):
        self.game = game
        self.spawn_position = position
        super().__init__(position=position, **kwargs)

        self.mode = mode  # '2d' or '3d'
        self.speed = 2
        self.timer = 0
        self.change_interval = GHOST_CHANGE_DIRECTION_INTERVAL
        self._health = GHOST_MAX_HEALTH
        self.max_health = GHOST_MAX_HEALTH

        self.original_color = ghost_color if ghost_color else color.red

        if self.mode == '2d':
            self.model = 'cube'
            self.texture = 'assrts/ghost2d/Textures/Ghost_Stencil.png'
            self.color = self.original_color
            self.scale = GHOST_SCALE_2D
            self.direction = Vec3(0, 0, 0)
        else:
            self.model = 'assrts/ghost3d/source/gh.fbx'
            self.texture = 'assrts/ghost3d/Textures/cl.jpeg'
            self.color = color.blue
            self.scale = Vec3(GHOST_SCALE_3D, GHOST_SCALE_3D, GHOST_SCALE_3D)
            self.rotation_x = -90
            self.direction = random.choice([
                Vec3(1, 0, 0), Vec3(-1, 0, 0),
                Vec3(0, 0, 1), Vec3(0, 0, -1)
            ])

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < 0:
            value = 0
        self._health = value

    def update(self):
        if not self.enabled or self.game.transition_in_progress:
            return
        self.timer += time.dt

        if self.mode == '3d':
            self.update_3d_behavior()
        else:
            self.update_2d_behavior()

    def choose_random_direction(self):
        if self.mode == '3d':
            directions = [Vec3(1,0,0), Vec3(-1,0,0), Vec3(0,0,1), Vec3(0,0,-1)]
        else:
            directions = [Vec3(1,0,0), Vec3(-1,0,0), Vec3(0,1,0), Vec3(0,-1,0)]
        self.direction = random.choice(directions)

    # ============= 2D =============
    def update_2d_behavior(self):
        if self.timer >= self.change_interval:
            self.timer = 0
            self.update_target_direction_2d()

        new_pos = self.position + self.direction * self.speed * time.dt
        if (not self.game.colliding_with_wall_2d(new_pos, self.scale / 2) # check if the ghost is colliding with the wall
                and not self.colliding_with_other_ghosts_2d(new_pos)):
            self.position = new_pos
        else:
            self.choose_random_direction()

    def update_target_direction_2d(self):
        ''' Update the direction of the ghost based on the pacman position '''
        dist_to_pac = distance(self.position, self.game.pacman.position) # distance to the pacman  - if the pacman is close enough - chase him
        if dist_to_pac < GHOST_ALERT_DISTANCE_2D:
            ghost_grid = self.game.world_to_grid_2d(self.position)
            pac_grid = self.game.world_to_grid_2d(self.game.pacman.position) # get the grid position of the pacman
            path = self.game.bfs_path(ghost_grid, pac_grid) # find the path to the pacman
            if path and len(path) > 1: 
                next_cell = path[1]
                next_world = self.game.grid_to_world_2d(next_cell[0], next_cell[1]) # get the world position of the next cell in the path
                dir_vec = next_world - self.position # calculate the direction vector to the next cell
                if dir_vec.length() > 0:
                    self.direction = dir_vec.normalized()
                else:
                    self.choose_random_direction()
            else:
                self.choose_random_direction()
        else:
            self.choose_random_direction()

    def colliding_with_other_ghosts_2d(self, new_pos: Vec3) -> bool: # check if the ghost is colliding with other ghosts
        for other in self.game.ghosts_2d:
            if other is self or not other.enabled:
                continue
            if distance(new_pos, other.position) < ((self.scale / 2) + (other.scale / 2)):
                return True
        return False

    # ============= 3D =============
    def update_3d_behavior(self):
        ''' Update the behavior of the ghost in 3D mode '''
        if self.timer >= self.change_interval:
            self.timer = 0
            self.update_target_direction_3d()

        future_pos = self.position + Vec3(self.direction.x, 0, self.direction.z) * self.speed * time.dt 
        if (not self.game.point_in_wall_3d(future_pos)
                and not self.colliding_with_other_ghosts_3d(future_pos)):
            self.position = future_pos
        else:
            self.choose_random_direction()

    def update_target_direction_3d(self):
        '''ghost behavior in 3D mode - chase the player'''
        if self.game.player_3d:
            pac_pos = Vec3(self.game.player_3d.position.x, 0, self.game.player_3d.position.z)
            ghost_pos = Vec3(self.position.x, 0, self.position.z)
            dist_to_pac = distance(ghost_pos, pac_pos)

            if dist_to_pac < GHOST_ALERT_DISTANCE_3D: # if the player is close enough to the ghost - chase him
                ghost_grid = self.game.world_to_grid_3d(self.position)
                pac_grid = self.game.world_to_grid_3d(self.game.player_3d.position)
                path = self.game.bfs_path(ghost_grid, pac_grid)
                if path and len(path) > 1: # if the path is found - move to the next cell
                    next_index = min(2, len(path) - 1)
                    next_cell = path[next_index]
                    next_world = self.game.grid_to_world_3d(next_cell[0], next_cell[1])
                    dir_vec = Vec3(next_world.x - self.position.x, 0, next_world.z - self.position.z)
                    if dir_vec.length() > 0: # if the direction is valid - move to the next cell in the path to the player
                        dir_vec = dir_vec.normalized()

                    future_pos = self.position + dir_vec * self.speed * time.dt # check if the future position is valid 
                    if (not self.game.point_in_wall_3d(future_pos)
                            and not self.colliding_with_other_ghosts_3d(future_pos)):
                        self.direction = dir_vec
                    else:
                        self.choose_random_direction()
                else:
                    self.choose_random_direction()
            else:
                self.choose_random_direction()
        else:
            self.choose_random_direction()

    def colliding_with_other_ghosts_3d(self, new_pos: Vec3) -> bool:
        '''check if the ghost is colliding with other ghosts'''
        for other in self.game.ghosts_3d:
            if other is self or not other or not other.enabled:
                continue
            if distance(new_pos, other.position) < 1.5:
                return True
        return False

    # ============= DAMAGE =============
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.game.sound_manager.play_ghost_death()
            self.disable()
