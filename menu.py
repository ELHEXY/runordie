# menu.py
# author: Elhex
#
# Description: Menu for the game. It has main menu, about us, record and name input screens

from ursina import *
from constants import ABOUT_US
import json
import os

SCOREBOARD_FILE = 'record.json'


class MenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(
            text=text,
            scale=(.25, .075),
            color=color.red.tint(-.25),
            highlight_color=color.black,
            pressed_color=color.azure.tint(+.25),
            text_origin=(0, 0),
            **kwargs
        )


class MainMenu(Entity):
    def __init__(self, start_game_callback=None, **kwargs):
        """ Main menu for the game.
        game does not start until player enters the name
        """
        super().__init__(parent=camera.ui, **kwargs)

        self.start_game_callback = start_game_callback
        self.player_name = ""

        # background for the main menu
        self.bg_main = Entity(
            parent=self,
            model='quad',
            texture='assrts/ckground/ck_menu.jpg',
            scale=(camera.aspect_ratio, 1),
            z=1,
            color=color.white
        )

        
        self.main_menu = Entity(parent=self, enabled=True)
        self.about_menu = Entity(parent=self, enabled=False)
        self.record_menu = Entity(parent=self, enabled=False)
        self.name_menu = Entity(parent=self, enabled=False)

        # background for the record menu
        self.bg_record = Entity(
            parent=self.record_menu,
            model='quad',
            scale=(camera.aspect_ratio, 1),
            z=0,
            texture='assrts/ckground/Record_back.jpg'
        )

        # buttons for the main menu
        self.start_btn = MenuButton(
            text='Start',
            parent=self.main_menu,
            y=0.1,
            on_click=self.on_start_clicked
        )
        self.record_btn = MenuButton(
            text='Record',
            parent=self.main_menu,
            y=-0.02,
            on_click=self.on_record_clicked
        )
        self.about_btn = MenuButton(
            text='About Us',
            parent=self.main_menu,
            y=-0.14,
            on_click=self.on_about_clicked
        )
        self.exit_btn = MenuButton(
            text='Exit',
            parent=self.main_menu,
            y=-0.26,
            on_click=self.on_exit_clicked
        )

        # about 
        self.about_text = Text(
            parent=self.about_menu,
            text=ABOUT_US,
            origin=(0, 0),
            y=0.1,
            scale=1,
            color=color.white,
            background=True,
            background_color=color.black,
            z=-1
        )
        self.about_back_btn = MenuButton(
            text='Back',
            parent=self.about_menu,
            y=-0.2,
            on_click=self.on_about_back_clicked
        )

        # input name screen
        self.name_label = Text(
            parent=self.name_menu,
            text='Enter your name:',
            origin=(0, 0),
            y=0.15,
            scale=1.2,
            color=color.white,
            background=True,
            background_color=color.black,
        )
        self.name_input = InputField(
            parent=self.name_menu,
            text='',
            scale=(.3, .08),
            color=color.black,
            y=0.02
        )
        self.name_ok_btn = MenuButton(
            text='OK',
            parent=self.name_menu,
            y=-0.15,
            on_click=self.on_name_ok_clicked
        )
        self.name_back_btn = MenuButton(
            text='Back',
            parent=self.name_menu,
            y=-0.28,
            on_click=self.on_name_back_clicked
        )

        self.record_text = Text(
            parent=self.record_menu,
            text='',
            origin=(0, 0),
            y=0.2,
            color=color.red,
            background=True,
            background_color=color.white,
            z=-1
        )
        self.record_back_btn = MenuButton(
            text='Back',
            parent=self.record_menu,
            y=-0.01,
            on_click=self.on_record_back_clicked
        )

    # ==== main menu click callbacks ====
    def on_start_clicked(self):
        self.main_menu.enabled = False
        self.name_menu.enabled = True

    def on_record_clicked(self):
        self.main_menu.enabled = False
        scoreboard = self.load_scoreboard()
        scoreboard_sorted = sorted(scoreboard, key=lambda x: x["score"], reverse=True)
        scoreboard_top5 = scoreboard_sorted[:5]

        scoreboard_text = "== SCOREBOARD ==\n"
        if scoreboard_top5:
            for entry in scoreboard_top5:
                scoreboard_text += f"{entry['name']}: {entry['score']}\n"
        else:
            scoreboard_text += "No records yet.\n"

        self.record_text.text = scoreboard_text
        self.record_text.position = (0, 0.5)
        self.record_text.animate_position((0, 0.2), duration=1, curve=curve.out_quint)
        self.record_menu.enabled = True

    def on_about_clicked(self):
        self.main_menu.enabled = False
        self.about_menu.enabled = True
        self.about_text.position = (0, 0.5)
        self.about_text.animate_position((0, 0.1), duration=1, curve=curve.out_quint)

    def on_exit_clicked(self):
        application.quit()

    # ==== ABOUT MENU callbacks =====
    def on_about_back_clicked(self):
        self.about_menu.enabled = False
        self.main_menu.enabled = True

    # ==== NAME MENU callbacks =====
    def on_name_ok_clicked(self):
        self.player_name = self.name_input.text.strip()
        if not self.player_name:
            self.player_name = "Unknown Player"
        self.disable_menu()
        if self.start_game_callback:
            self.start_game_callback()

    def on_name_back_clicked(self):
        self.name_menu.enabled = False
        self.main_menu.enabled = True

    # ==== RECORD MENU callbacks ====
    def on_record_back_clicked(self):
        self.record_menu.enabled = False
        self.main_menu.enabled = True

    # ==== general ====
    def disable_menu(self):
        self.enabled = False

    def load_scoreboard(self):
        if not os.path.exists(SCOREBOARD_FILE):
            return []
        try:
            with open(SCOREBOARD_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Malformed JSON in {SCOREBOARD_FILE}")
            return []

    def save_scoreboard(self, scoreboard):
        try:
            with open(SCOREBOARD_FILE, 'w') as f:
                json.dump(scoreboard, f, indent=4)
        except Exception:
            pass

    def add_player_result(self, player_name, score):
        if not player_name:
            player_name = "Unknown Player"
        scoreboard = self.load_scoreboard()
        scoreboard.append({"name": player_name, "score": score})
        scoreboard = sorted(scoreboard, key=lambda x: x["score"], reverse=True)
        self.save_scoreboard(scoreboard)
