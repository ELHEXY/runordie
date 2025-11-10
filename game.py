# game.py
# author: Elhex
#
# Description: The main game logic: collisions, pathfinding, transitions 2D/3D.

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math, random, time
from collections import deque

from constants import *
from pellets import Pellet, PowerPellet
from pacman import PacMan
from ghost import Ghost
from bullet import Bullet
from video import VideoPlayer
from sound_manager import SoundManager


class PacManGame(Entity):
    def __init__(self, menu=None):
        super().__init__()  # call the parent class constructor
        self.menu = menu

        self.sound_manager = SoundManager()
        self.sound_manager.play_music('menu')

        self.mode3d = False
        self.transition_in_progress = False

        # --- 2D objects ---
        self.floor_2d = []
        self.walls = []
        self.pellets = []
        self.power_pellets = []
        self.ghosts_2d = []
        self.pacman = None

        # --- 3D objects ---
        self.sky = None
        self.player_3d = None
        self.ground = None
        self.walls_3d = []
        self.pellets_3d = []
        self.ghosts_3d = []
        self.bullets_3d = []
        self.gun = None

        # bullet pool for 3D
        self.bullet_pool = []

        # map data
        self.level_data = LEVEL_DATA

        # BFS grid for 2D
        self.grid_2d = []
        self.rows_2d = 0
        self.cols_2d = 0

        self.ghost_spawn_positions = []

        # Text for Win / Game Over
        self.win_text = Text(
            parent=camera.ui,
            text='You Win! Your score: 0',
            origin=(0, 0),
            scale=2,
            color=color.white,
            background=True,
            background_color=color.black,
            z=-9999
        )
        self.win_text.enabled = False

        self.game_over_text = None

        # pause menu
        self.pause_menu = Entity(parent=camera.ui, enabled=False)
        self.pause_bg = Entity(
            parent=self.pause_menu,
            model='quad',
            texture='assrts/ckground/ck_menu.jpg',
            scale=(2, 2),
            z=0.5
        )
        self.resume_button = Button(
            parent=self.pause_menu,
            text='Resume',
            scale=(0.2, 0.08),
            y=0.05,
            on_click=self.toggle_pause
        )
        self.exit_button = Button(
            parent=self.pause_menu,
            text='Exit',
            scale=(0.2, 0.08),
            y=-0.07,
            on_click=application.quit
        )

        #create level and objects
        self.create_bfs_grid()
        self.create_2d_level()
        self.compute_level_center()

    # ===================================================================
    # 2D / 3D Level Creation
    # ===================================================================
    def create_bfs_grid(self):
        """create 2D grid for BFS pathfinding"""
        rows = len(self.level_data)
        if rows < 1:
            return
        cols = len(self.level_data[0])
        self.grid_2d = []
        for y, row_str in enumerate(self.level_data):
            row_str = row_str.rstrip('\n')
            line = []
            for ch in row_str:
                line.append(ch == 'W')
            self.grid_2d.append(line)
        self.rows_2d = rows
        self.cols_2d = cols

    def create_2d_level(self):
        ghost_count = 0
        max_ghosts = 4

        for y, row in enumerate(self.level_data):
            row = row.rstrip('\n')
            for x, cell in enumerate(row):
                px = (x - len(row) // 2) * 2
                py = (len(self.level_data) // 2 - y) * 2
                pos = Vec3(px, py, 0)

                floor_tile = Entity(
                    model='quad',
                    color=color.gray,
                    scale=(2, 2),
                    position=pos,
                    rotation_x=90
                )
                self.floor_2d.append(floor_tile)

                if cell == 'W':
                    wall = Entity(
                        model='cube',
                        color=color.blue,
                        scale=(2, 2, 2),
                        position=pos,
                        collider='box'
                    )
                    self.walls.append(wall)
                elif cell == 'P':
                    pellet = Pellet(pos)
                    self.pellets.append(pellet)
                elif cell == 'O':
                    power_pellet = PowerPellet(pos)
                    self.power_pellets.append(power_pellet)
                elif cell == 'M':
                    if not self.pacman:
                        self.pacman = PacMan(pos, game=self)
                elif cell == 'G':
                    if ghost_count < max_ghosts:
                        self.ghost_spawn_positions.append(pos)
                        ghost_count += 1

        ghost_colors = [color.red, color.pink, color.cyan, color.orange]
        for i, spawn_pos in enumerate(self.ghost_spawn_positions):
            new_ghost = Ghost(spawn_pos, mode='2d', game=self, ghost_color=ghost_colors[i % len(ghost_colors)])
            self.ghosts_2d.append(new_ghost)

        camera.position = CAMERA_2D_POSITION
        camera.fov = CAMERA_2D_FOV
        camera.rotation_x = CAMERA_2D_ROTATION_X

    def create_labyrinth_3d(self):
        """3d maze creation based on 2d level data."""
        self.walls_3d.clear()
        wall_height = WALL_HEIGHT
        rows = len(self.level_data)
        cols = len(self.level_data[0].strip())
        for y, row in enumerate(self.level_data):
            row = row.strip()
            for x, cell in enumerate(row):
                if cell == 'W':
                    px = (x - cols // 2) * 2
                    pz = (rows // 2 - y) * 2
                    pos = Vec3(px, wall_height / 2, pz)
                    w = Entity(
                        model='cube',
                        texture='assrts/walls/Textures/BaseColor.png',
                        color=color.gray,
                        scale=(2, wall_height, 2),
                        position=pos,
                        collider='box'
                    )
                    self.walls_3d.append(w)

    def compute_level_center(self):
        """compute the center of the level based on the 2D grid for 3D camera positioning"""
        positions = []
        for y, row in enumerate(self.level_data):
            row = row.strip()
            for x, _ in enumerate(row):
                px = (x - len(row) // 2) * 2
                pz = (len(self.level_data) // 2 - y) * 2
                positions.append(Vec3(px, 0, pz))
        if positions:
            avg_x = sum(p.x for p in positions) / len(positions)
            avg_z = sum(p.z for p in positions) / len(positions)
            self.level_center = Vec3(avg_x, 0, avg_z)
        else:
            self.level_center = Vec3(0, 0, 0)

    # ===================================================================
    # BFS / Pathfinding
    # ===================================================================
    def is_wall_2d(self, c, r):
        """check if the cell (r,c) is a wall in the 2D grid"""
        if r < 0 or r >= self.rows_2d or c < 0 or c >= self.cols_2d:
            return True
        return self.grid_2d[r][c]

    def bfs_path(self, start, goal):
        """BFS pathfinding algorithm (2D)."""
        if self.is_wall_2d(start[0], start[1]) or self.is_wall_2d(goal[0], goal[1]):
            return None
        from collections import deque
        visited = set()
        queue = deque()
        queue.append((start, [start]))
        visited.add(start)

        while queue:
            (cx, cy), path = queue.popleft()
            if (cx, cy) == goal:
                return path
            for (nx, ny) in [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
                if not self.is_wall_2d(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return None

    def world_to_grid_2d(self, world_pos):
        halfCols = self.cols_2d // 2
        halfRows = self.rows_2d // 2
        col = int(round(world_pos.x / 2 + halfCols))
        row = int(round(halfRows - world_pos.y / 2))
        return (col, row)

    def grid_to_world_2d(self, c, r):
        halfCols = self.cols_2d // 2
        halfRows = self.rows_2d // 2
        px = (c - halfCols) * 2
        py = (halfRows - r) * 2
        return Vec3(px, py, 0)

    def world_to_grid_3d(self, world_pos):
        halfCols = self.cols_2d // 2
        halfRows = self.rows_2d // 2
        col = int(round(world_pos.x / 2 + halfCols))
        row = int(round(halfRows - world_pos.z / 2))
        return (col, row)

    def grid_to_world_3d(self, c, r):
        halfCols = self.cols_2d // 2
        halfRows = self.rows_2d // 2
        px = (c - halfCols) * 2
        pz = (halfRows - r) * 2
        return Vec3(px, 0, pz)

    # ===================================================================
    # UPDATE
    # ===================================================================
    def update(self):
        """update game logic based on the mode (2D / 3D) and collisions"""
        if self.mode3d:
            self.update_3d_collisions()
        else:
            self.update_2d_collisions()

        # pellets eaten check for win condition 
        if (not self.mode3d
           and len(self.pellets) == 0
           and len(self.power_pellets) == 0
           and not self.win_text.enabled):
            self.handle_win()

    def update_2d_collisions(self):
        if self.transition_in_progress or not self.pacman:
            return

        # eat pellets
        for p in self.pellets[:]:
            if distance(self.pacman.position, p.position) < PELLET_EAT_DISTANCE:
                self.pacman.score += EAT_PELLET_SCORE
                p.disable()
                self.pellets.remove(p)

        # Power-pellets
        for pp in self.power_pellets[:]:
            if distance(self.pacman.position, pp.position) < PELLET_EAT_DISTANCE:
                self.pacman.score += EAT_POWER_PELLET_SCORE
                pp.disable()
                self.power_pellets.remove(pp)

                # win or shift to 3D 
                if len(self.pellets) == 0 and len(self.power_pellets) == 0:
                    self.handle_win()
                    return

                self.shift_to_3d_video()

        # coollision with walls 
        for g in self.ghosts_2d:
            if distance(self.pacman.position, g.position) < PELLET_EAT_DISTANCE:
                self.handle_game_over()
                return

    def update_3d_collisions(self):
        if self.transition_in_progress or not self.player_3d:
            return
        # eat pellets
        ph = Vec3(self.player_3d.position.x, 0, self.player_3d.position.z)
        for p in self.pellets_3d[:]:
            pp = Vec3(p.position.x, 0, p.position.z)
            if distance(ph, pp) < PELLET_EAT_DISTANCE:
                self.pacman.score += EAT_PELLET_SCORE
                p.disable()
                self.pellets_3d.remove(p)

    # ===================================================================
    # COLLISION HELPER
    # ===================================================================
    def colliding_with_wall_2d(self, pos, radius):
        """check if the position pos is colliding with a wall (2D)"""
        for w in self.walls:
            half_w = w.scale_x / 2
            half_h = w.scale_y / 2
            cx = max(w.x - half_w, min(pos.x, w.x + half_w))
            cy = max(w.y - half_h, min(pos.y, w.y + half_h))
            if math.dist((pos.x, pos.y), (cx, cy)) < radius:
                return True
        return False

    def point_in_wall_3d(self, pos):
        """check if the position pos is inside a wall (3D)"""
        ghost_size = 0.5
        for w in self.walls_3d:
            minx = w.x - w.scale_x / 2 - ghost_size
            maxx = w.x + w.scale_x / 2 + ghost_size
            minz = w.z - w.scale_z / 2 - ghost_size
            maxz = w.z + w.scale_z / 2 + ghost_size
            if (minx <= pos.x <= maxx) and (minz <= pos.z <= maxz):
                return True
        return False

    # ===================================================================
    # SHIFTING BETWEEN 2D / 3D
    # ===================================================================
    def shift_to_3d_video(self):
        """play video and shift to 3D mode"""
        self.transition_in_progress = True
        self.video_player = VideoPlayer(
            frames_folder=PORTAL_FRAMES_FOLDER,
            fps=VIDEO_FPS_2D_TO_3D,
            on_finish=self.enable_3d
        )
        self.sound_manager.play_transition_2d_to_3d()

    def enable_3d(self):
        """2d -> 3d transition"""
        self.mode3d = True
        self.sound_manager.play_music('3d')

        # disable 2D objects
        if self.pacman:
            self.pacman.enabled = False
        for tile in self.floor_2d:
            tile.enabled = False
        for w in self.walls:
            w.enabled = False
        for p in self.pellets:
            p.enabled = False
        for pp in self.power_pellets:
            pp.enabled = False
        for g in self.ghosts_2d:
            g.enabled = False

        # 3D camera
        camera.orthographic = False
        camera.fov = CAMERA_3D_FOV
        camera.position = CAMERA_3D_POSITION
        camera.rotation_x = CAMERA_3D_ROTATION_X

        # create 3D objects
        self.sky = Sky()
        pos_3d = Vec3(self.level_center.x, PLAYER_START_Y, self.level_center.z)
        self.player_3d = FirstPersonController(y=PLAYER_START_Y, origin_y=FPS_CONTROLLER_ORIGIN_Y)
        self.player_3d.position = pos_3d
        self.player_3d.collider = 'box'

        self.ground = Entity(
            model="plane",
            scale=GROUND_SCALE,
            color=color.white,
            texture='assrts/Floor/Floor.png',
            texture_scale=(GROUND_SCALE[0], GROUND_SCALE[2]),
            collider='box',
            position=(self.level_center.x, GROUND_Y, self.level_center.z)
        )
        self.create_labyrinth_3d()

        from constants import GUN_3D_MODEL, GUN_3D_TEXTURE, GUN_3D_SCALE
        self.gun = Entity(
            model=GUN_3D_MODEL,
            texture=GUN_3D_TEXTURE,
            scale=GUN_3D_SCALE,
            parent=camera.ui,
            position=(0.3, -0.2),
            rotation=(0, -70, 0)
        )

        # create 3D pellets
        self.pellets_3d = []
        for x in range(-15, 16, 5):
            for z in range(-15, 16, 5):
                pos_check = Vec3(x, 0, z)
                if not self.point_in_wall_3d(pos_check):
                    e = Entity(
                        model='sphere',
                        color=color.yellow,
                        scale=0.7,
                        position=(x, 1, z)
                    )
                    self.pellets_3d.append(e)

        # create 3D ghosts
        self.ghosts_3d = []
        max_3d_ghosts = 4
        spawn_attempts = 10
        while len(self.ghosts_3d) < max_3d_ghosts and spawn_attempts > 0:
            rx = random.randint(-10, 10)
            rz = random.randint(-10, 10)
            sp = Vec3(rx, 0, rz)
            if not self.point_in_wall_3d(sp) and not any(distance(sp, g.position) < 2 for g in self.ghosts_3d):
                g3d = Ghost(sp, mode='3d', game=self)
                self.ghosts_3d.append(g3d)
            spawn_attempts -= 1

        # bullets pool for 3D mode
        self.bullets_3d = self.bullet_pool
        invoke(self.shift_to_2d_video, delay=SHIFT_BACK_TO_2D_DELAY)
        self.transition_in_progress = False

    def shift_to_2d_video(self):
        """play video and shift to 2D mode"""
        self.sound_manager.play_transition_3d_to_2d()
        self.transition_in_progress = True
        self.video_player = VideoPlayer(
            frames_folder=PORTAL_FRAMES_FOLDER,
            fps=VIDEO_FPS_3D_TO_2D,
            on_finish=self.enable_2d
        )

    def enable_2d(self):
        """3d -> 2d transition"""
        self.sound_manager.play_music('2d')
        if getattr(self, 'video_player', None):
            destroy(self.video_player)
            self.video_player = None

        #disable 3D objects
        if self.sky:
            destroy(self.sky)
            self.sky = None
        if self.player_3d:
            destroy(self.player_3d)
            self.player_3d = None
        if self.ground:
            destroy(self.ground)
            self.ground = None
        for w in self.walls_3d:
            destroy(w)
        self.walls_3d.clear()

        for p in self.pellets_3d:
            destroy(p)
        self.pellets_3d.clear()

        for g in self.ghosts_3d:
            destroy(g)
        self.ghosts_3d.clear()

        for b in self.bullets_3d:
            destroy(b)
        self.bullets_3d.clear()

        if self.gun:
            destroy(self.gun)
            self.gun = None

        # enable 2D objects
        if self.pacman:
            self.pacman.enabled = True
        for tile in self.floor_2d:
            tile.enabled = True
        for w in self.walls:
            w.enabled = True
        for p in self.pellets:
            p.enabled = True
        for pp in self.power_pellets:
            pp.enabled = True
        for g in self.ghosts_2d:
            g.enabled = True

        camera.orthographic = True
        camera.fov = CAMERA_2D_FOV
        camera.position = CAMERA_2D_POSITION
        camera.rotation_x = CAMERA_2D_ROTATION_X
        camera.clear_color = color.black

        self.mode3d = False
        self.transition_in_progress = False

    # ===================================================================
    # BULLETS / GHOST HELPERS
    # ===================================================================
    def respawn_ghost(self, spawn_position, mode, ghost_color):
        """Respawn ghost at given position"""
        if mode == '2d':
            if len(self.ghosts_2d) < 4:
                ng = Ghost(spawn_position, mode='2d', game=self, ghost_color=ghost_color)
                self.ghosts_2d.append(ng)
        else:
            if len(self.ghosts_3d) < 4:
                ng = Ghost(spawn_position, mode='3d', game=self, ghost_color=ghost_color)
                self.ghosts_3d.append(ng)

    def get_bullet(self, bullet_start, direction):
        """taking a bullet from the pool or creating a new one"""
        for bullet in self.bullet_pool:
            if not bullet.enabled:
                bullet.position = bullet_start
                bullet.direction = direction.normalized()
                bullet.life_time = 2
                bullet.enable()
                return bullet
        new_bullet = Bullet(position=bullet_start, direction=direction, game=self)
        self.bullet_pool.append(new_bullet)
        return new_bullet

    # ===================================================================
    # INPUT / PAUSE
    # ===================================================================
    def input(self, key):
        """handle input for pause, shooting, and game restart"""
        if key == 'escape':
            if not self.win_text.enabled:
                self.toggle_pause()

        if self.mode3d and not self.transition_in_progress and key == 'left mouse down':
            self.sound_manager.play_shoot()
            bullet_start = camera.world_position
            self.get_bullet(bullet_start, camera.forward)

    def toggle_pause(self):
        """pause / unpause the game"""
        self.pause_menu.enabled = not self.pause_menu.enabled
        application.paused = self.pause_menu.enabled

    # ===================================================================
    # WIN / GAME OVER / RESTART
    # ===================================================================
    def handle_win(self):
        """handle win condition"""
        if self.menu:
            self.menu.add_player_result(self.menu.player_name, self.pacman.score)
        self.win_text.text = f"You Win!\nYour Score: {self.pacman.score}"
        self.win_text.enabled = True
        self.win_text.color = color.white
        self.win_text.z = -1
        self.create_buttons()
        application.pause()

    def handle_game_over(self):
        """handle game over condition"""
        if self.menu:
            self.menu.add_player_result(self.menu.player_name, self.pacman.score)
        application.pause()
        self.game_over_text = Text(
            f"Game Over!\nYour Score: {self.pacman.score}",
            origin=(0, 0),
            scale=2,
            color=color.red,
            background=True,
            background_color=color.black
        )
        self.create_buttons()

    def create_buttons(self):
        """create restart / exit buttons for win / game over screens"""
        if not hasattr(self, 'win_restart_btn'):
            self.win_restart_btn = Button(
                parent=camera.ui,
                text="Restart",
                scale=(0.2, 0.08),
                y=-0.2,
                on_click=self.restart_game
            )
        if not hasattr(self, 'win_exit_btn'):
            self.win_exit_btn = Button(
                parent=camera.ui,
                text="Exit",
                scale=(0.2, 0.08),
                y=-0.3,
                on_click=application.quit
            )

    def restart_game(self):
        application.paused = False
        self.sound_manager.stop_all_music()

        # destroy buttons
        for attr in ['win_restart_btn', 'win_exit_btn', 'game_over_restart_btn', 'game_over_exit_btn']:
            if hasattr(self, attr):
                destroy(getattr(self, attr))
                delattr(self, attr)

        if self.win_text:
            destroy(self.win_text)
            self.win_text = None
        if self.game_over_text:
            destroy(self.game_over_text)
            self.game_over_text = None

        # destroy 2D objects
        for obj in ([self.pacman] + self.ghosts_2d + self.ghosts_3d +
                    self.floor_2d + self.walls + self.pellets + self.power_pellets):
            if obj:
                destroy(obj)

        destroy(self)

        # call the start game callback
        if self.menu and self.menu.start_game_callback:
            self.menu.start_game_callback()

    def exit_game(self):
        application.quit()
