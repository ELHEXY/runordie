# main.py
# author: Elhex
#
# Description: Main entry point for the game.

from ursina import *
from constants import FOV, CAMERA_POSITION, CAMERA_ORTHOGRAPHIC
from menu import MainMenu
from preloader import preload_resources  

def start_game():
    """
    Start the game and disable the menu
    """
    menu.disable_menu()
    from game import PacManGame
    local_game = PacManGame(menu=menu)
    menu.game_instance = local_game


if __name__ == '__main__':
    app = Ursina(development_mode=False)  # disable dev mode
    preload_resources()
    camera.orthographic = CAMERA_ORTHOGRAPHIC
    camera.fov = FOV
    camera.position = CAMERA_POSITION

    menu = MainMenu(start_game_callback=start_game)

    app.run()

