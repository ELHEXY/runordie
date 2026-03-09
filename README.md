#Run or Die

###Author: Elhex

"RUN OR DIE" is a Pac-Man-inspired game built using the Ursina Engine. The project features two gameplay modes: 2D and 3D. On startup, the main menu is displayed, allowing the user to start the game, view records, read game information, or exit the application.
-------------------------------------------------------------------------------------------------------------
					
##REQUIREMENTS

	-Python 3.10 (or newer)
	-Ursina Engine (version 4.x or newer)

Install using:

	pip install ursina

For MacOS, please ensure that Python has permission to display graphical windows.
-------------------------------------------------------------------------------------------------------------

##RUNNING THE PROJECT

Download or clone the project repository to your machine.
Ensure all dependencies are installed (see Requirements).
Navigate to the project root directory (where main.py is located).
Run the project with the command:

	python main.py

-------------------------------------------------------------------------------------------------------------

##BASIC CONTROLS
Main Menu:

	- Start – Launches the game (you will be prompted to enter your name).
	- Record – Displays the scoreboard.
	- About – Shows information about the game.
	- Exit – Exits the application.

In 2D Mode:

	- W, A, S, D – Move Pac-Man along the level.
	- When all pellets are collected, a "You Win!" message is displayed.

In 3D Mode:
	
	- Movement is similar to a first-person shooter (using the built-in FirstPersonController).
	- Left Mouse Button – Shoot.
-------------------------------------------------------------------------------------------------------------

##ADDITIONAL NOTES

- The project implements resource preloading (textures, models, and video frames). This preloading may take a few moments before the main menu appears, but it helps ensure smooth gameplay without delays or freezes.
- The project has been tested on both Windows and MacOS.
- The record.json file is created automatically when records are first saved.
---------------------------------------------------------------------------------------------------------------
					 
##RARE ISSUE

-Occasionally, when transitioning from 2D to 3D mode, the player may fall infinitely into the void.

Solution:
	If this happens, simply restart the game by closing and reopening it.
	Unfortunately, this bug could not be resolved within the project timeframe.
