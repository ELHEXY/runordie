# test_game.py
# author: Elhex
#
# Description: Unit tests for the game functionality (game.py, ghost.py, pacman.py, bullet.py)

import unittest
import os
from ursina import Ursina, Vec3
from game import PacManGame
from ghost import Ghost
from pacman import PacMan
from bullet import Bullet
from menu import MainMenu


class TestGameLogic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Initialize Ursina once before running all tests.
        """
        cls.app = Ursina(development_mode=True)

    def setUp(self):
        """
        Create a fresh instance of PacManGame before each test.
        """
        self.game = PacManGame()
        self.game.create_2d_level()

    # ---------- BFS TESTS ----------
    def test_bfs_path_normal(self):
        """
        Check that BFS returns a valid path between two walkable cells.
        """
        start = (2, 1)  # 'P'
        goal = (12, 1)  # also 'P'
        path = self.game.bfs_path(start, goal)
        self.assertIsNotNone(path, "BFS should return a path between (2,1) and (12,1).")
        self.assertGreater(len(path), 1, "Path should have multiple steps.")

    def test_bfs_path_no_path(self):
        """
        Check that BFS returns None if the goal is behind a wall or out of bounds.
        """
        start = (2, 1)  # 'P'
        goal = (13, 1)  # col=13 in row=1 is 'W' => a wall
        path = self.game.bfs_path(start, goal)
        if path is not None:
            self.fail("Expected no path because (13,1) is a wall, but BFS returned a non-None path.")

    def test_bfs_path_same_start_goal(self):
        """
        If start == goal and it's a valid (walkable) cell, BFS may return
        """
        same_cell = (2, 1)  # 'P'
        path = self.game.bfs_path(same_cell, same_cell)
        self.assertIsNotNone(path, "BFS should not return None when start == goal.")
        self.assertEqual(len(path), 1, "Path should have exactly one element (the same cell).")

    # ---------- GHOST TESTS ----------
    def test_ghost_damage_property(self):
        """
        Check that a Ghost correctly applies damage via the health property,
        and disables itself when health reaches 0.
        """
        ghost = Ghost(position=Vec3(0, 0, 0), mode='2d', game=self.game)
        self.assertEqual(ghost.health, ghost.max_health)

        ghost.take_damage(5)
        expected_health = ghost.max_health - 5
        self.assertEqual(
            ghost.health, expected_health,
            f"Ghost health should be {expected_health} after taking 5 damage."
        )

        ghost.take_damage(999)
        self.assertEqual(
            ghost.health, 0,
            "Ghost health should not go below 0. The setter should clamp it."
        )
        self.assertFalse(ghost.enabled, "Ghost should disable itself at 0 health.")

    # ---------- PACMAN TESTS ----------
    def test_pacman_score_property(self):
        """
        Check that PacMan's score property (getter/setter) works correctly.
        """
        pacman = PacMan(Vec3(2, 0, 0), self.game)
        self.assertEqual(pacman.score, 0, "Initial PacMan score should be 0.")

        pacman.score = 10
        self.assertEqual(pacman.score, 10, "PacMan score should update to 10.")

        pacman.score = -50
        self.assertEqual(
            pacman.score, 0,
            "Setter should not allow the score to go below 0; it should be clamped."
        )

    # ---------- BULLET TESTS ----------
    def test_bullet_lifetime(self):
        """
        Check that a bullet disables itself once its lifetime expires.
        """
        bullet = Bullet(position=Vec3(0, 0, 0), direction=Vec3(1, 0, 0), game=self.game)
        self.assertTrue(bullet.enabled, "Bullet should be enabled upon creation.")

        bullet.life_time = -1
        bullet.update()
        self.assertFalse(bullet.enabled, "Bullet should disable when life_time <= 0.")

    # ---------- COLLISION TESTS ----------
    def test_pacman_wall_collision(self):
        """
        Check that PacMan does not walk through walls.
        """
        pacman = PacMan(Vec3(0, 0, 0), self.game)
        pacman.direction = Vec3(1, 0, 0)
        old_pos = pacman.position

        for _ in range(10):
            pacman.update()

        distance_moved = (pacman.position - old_pos).length()
        self.assertLessEqual(
            distance_moved, 0.1,
            "PacMan should not be able to pass through the wall."
        )

    # ---------- MENU / SCOREBOARD TESTS ----------
    def test_menu_load_scoreboard(self):
        """
        Simple test for loading scoreboard via MainMenu's load_scoreboard() method.
        It should return a list, possibly empty, if no records exist yet.
        """
        menu = MainMenu()
        scoreboard = menu.load_scoreboard()
        self.assertIsInstance(scoreboard, list, "load_scoreboard should return a list.")


if __name__ == '__main__':
    unittest.main()
