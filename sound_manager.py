# sound_manager.py
# author: Elhex
#
# Description: Manages all sounds and music in the game.

from ursina import *
from constants import SHOOT_SOUND, GHOST_DEATH_SOUND, TRANSITION_2D_TO_3D_SOUND, TRANSITION_3D_TO_2D_SOUND, MAIN_MUSIC, THREED_MUSIC


class SoundManager:
    def __init__(self):
        # sounds
        self.shoot_sound = Audio(SHOOT_SOUND, autoplay=False)
        self.ghost_death_sound = Audio(GHOST_DEATH_SOUND, autoplay=False)
        self.transition_2d_to_3d = Audio(TRANSITION_2D_TO_3D_SOUND, autoplay=False)
        self.transition_3d_to_2d = Audio(TRANSITION_3D_TO_2D_SOUND, autoplay=False)

        # background music
        self.current_music = None
        self.menu_music = Audio(MAIN_MUSIC, loop=True, autoplay=False)
        self.music_2d = Audio(MAIN_MUSIC, loop=True, autoplay=False)
        self.music_3d = Audio(THREED_MUSIC, loop=True, autoplay=False)

    def play_shoot(self):
        self.shoot_sound.play()

    def play_ghost_death(self):
        self.ghost_death_sound.play()

    def play_transition_2d_to_3d(self):
        self.stop_all_music()
        self.transition_2d_to_3d.play()

    def play_transition_3d_to_2d(self):
        self.stop_all_music()
        self.transition_3d_to_2d.play()

    def play_music(self, mode):
        if self.current_music:
            self.current_music.stop()

        if mode == 'menu':
            self.current_music = self.menu_music
        elif mode == '2d':
            self.current_music = self.music_2d
        elif mode == '3d':
            self.current_music = self.music_3d

        if self.current_music:
            self.current_music.play()

    def stop_all_music(self):
        if self.current_music:
            self.current_music.stop()
        self.current_music = None
