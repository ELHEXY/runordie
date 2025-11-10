# constants.py
# author: Elhex
#
# Description: Constants for the game, including level data, magic numbers, resource paths, etc.

# ------------ Level data -------------
LEVEL_DATA = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WMPPPPPPPPPPPWWPPPPPPPPPPPPW",
    "WPWWWWPWWWWWPWWPWWWWWPWWWWOW",
    "WPWWWWPPPPPPPPPPPPPPPPPPPPPW",
    "WPWWWWPWWPWWWWWWWWPWWPWWWWPW",
    "WPPPPPPWWPPPPPPPPPPWWPPPPPPW",
    "WWWWWWPWWWW      WWWWPWWWWWW",
    "WWWWWWPWW          WWPWWWWWW",
    "WWWWWWPWWPWW    WWPWWPWWWWWW",
    "WPPPPPPPPPW      WPPPPPPPPPW",
    "WWWWWWPWWPW GGGG WPWWPWWWWWW",
    "WPPPPPPPPPWWWWWWWWPPPPPPPPPW",
    "WPWWWWPWWWWWWWWWWWWWWPWWWWPW",
    "WPPPWWPPPPPPPPPPPPPPPPWWPPPW",
    "WWWPWWPWWPWWWWWWWWPWWPWWPWWW",
    "WPPPPPPWWPPPPWWPPPPWPPPPPPPW",
    "WPWWWWWWWWWWPWWPWWWWWWWWWWPW",
    "WPPPPPPPPPPPPPPPPPPPPPPPPPPW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# ------------ Level sizes -------------
GROUND_SCALE = (80, 1, 80)
GROUND_Y = 0
WALL_HEIGHT = 8
# ------------ Player 3D -------------
PLAYER_START_Y = 5
FPS_CONTROLLER_ORIGIN_Y = -0.5

# ------------ Camera -------------
CAMERA_3D_FOV = 90
CAMERA_3D_POSITION = (0, 15, -30)
CAMERA_3D_ROTATION_X = 20

CAMERA_2D_FOV = 40
CAMERA_2D_POSITION = (0, 0, -50)
CAMERA_2D_ROTATION_X = 0

FOV = 20
CAMERA_POSITION = (0, 0, -40)
CAMERA_ORTHOGRAPHIC = True

# ------------ Score & collisions -------------
PELLET_EAT_DISTANCE = 1.5
EAT_PELLET_SCORE = 10
EAT_POWER_PELLET_SCORE = 50

# ------------ Ghost -------------
GHOST_ALERT_DISTANCE_2D = 25
GHOST_ALERT_DISTANCE_3D = 25
GHOST_CHANGE_DIRECTION_INTERVAL = 1   # seconds
GHOST_MAX_HEALTH = 10

# ------------ 3D spawn attempts -------------
SPAWN_RANGE_3D = 10
SPAWN_ATTEMPTS_3D = 10

# ------------ Bullet -------------
BULLET_LIFETIME = 2
BULLET_COLLISION_DISTANCE_3D = 1.5

# ------------ Ghost scale -------------
GHOST_SCALE_2D = 1.8
GHOST_SCALE_3D = 0.5

# ------------ Transition / Video -------------
PORTAL_FRAMES_FOLDER = 'assrts/portal_frames'
VIDEO_FPS_2D_TO_3D = 20
VIDEO_FPS_3D_TO_2D = 20
SHIFT_BACK_TO_2D_DELAY = 15   # seconds

# ------------ Gun -------------
GUN_3D_MODEL = 'assrts/gun3d/source/colt low polyfbx.fbx'
GUN_3D_TEXTURE = 'assrts/gun3d/Textures/colt_low_polyfbx_m1911_BaseColor.png'
GUN_3D_SCALE = 0.0009

# ------------ About text -------------
ABOUT_US = '''Pac-Man — a game developed by ElHex.
Inspired by the classics, it combines timeless gameplay with modern 2D and 3D modes.
Every detail has been carefully designed to deliver an engaging and immersive gaming experience.
Enjoy the game!'''

# ------------ Sounds -------------
SHOOT_SOUND = 'assrts/sounds/laser_sound.wav'
GHOST_DEATH_SOUND = 'assrts/sounds/ghost_d.mp3'
TRANSITION_2D_TO_3D_SOUND = 'assrts/sounds/TwoDtothreeD.wav'
TRANSITION_3D_TO_2D_SOUND = 'assrts/sounds/ThreeDtotwoD.wav'
MAIN_MUSIC = 'assrts/sounds/Main.wav'
THREED_MUSIC = 'assrts/sounds/ThreeD.wav'
