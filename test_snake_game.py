import unittest
import tkinter as tk
from unittest.mock import patch

import snake_game


class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        # Prevent the automatic game loop from starting during tests
        self.loop_patcher = patch.object(snake_game.SnakeGame, "game_loop", lambda self: None)
        self.loop_patcher.start()

        self.root = tk.Tk()
        self.root.withdraw()  # hide the window during tests
        self.game = snake_game.SnakeGame(self.root)

    def tearDown(self):
        self.loop_patcher.stop()
        self.root.destroy()

    def test_normal_food_increases_score_by_one(self):
        self.game.score = 0
        self.game.food_type = "normal"
        self.game.handle_food_effect()
        self.assertEqual(self.game.score, 1)

    def test_bonus_food_increases_score_by_three(self):
        self.game.score = 0
        self.game.food_type = "bonus"
        self.game.handle_food_effect()
        self.assertEqual(self.game.score, 3)

    def test_slow_food_activates_slow_timer(self):
        self.game.score = 0
        self.game.food_type = "slow"
        self.game.handle_food_effect()
        self.assertEqual(self.game.score, 1)
        self.assertEqual(self.game.slow_timer, snake_game.POWER_UP_DURATION)

    def test_ghost_food_activates_ghost_timer(self):
        self.game.score = 0
        self.game.food_type = "ghost"
        self.game.handle_food_effect()
        self.assertEqual(self.game.score, 1)
        self.assertEqual(self.game.ghost_timer, snake_game.POWER_UP_DURATION)

    def test_wall_collision_is_detected(self):
        self.assertTrue(self.game.check_collision((-1, 5)))
        self.assertTrue(self.game.check_collision((5, -1)))
        self.assertTrue(self.game.check_collision((snake_game.GRID_WIDTH, 5)))
        self.assertTrue(self.game.check_collision((5, snake_game.GRID_HEIGHT)))

    def test_self_collision_is_detected(self):
        self.game.snake = [(5, 5), (4, 5), (4, 6), (5, 6)]
        self.assertTrue(self.game.check_collision((4, 5)))

    def test_obstacle_collision_detected_without_ghost(self):
        self.game.score = 6
        self.game.generate_obstacles()
        self.game.ghost_timer = 0
        obstacle = next(iter(self.game.obstacles))
        self.assertTrue(self.game.check_collision(obstacle))

    def test_obstacle_collision_not_detected_with_ghost(self):
        self.game.score = 6
        self.game.generate_obstacles()
        self.game.ghost_timer = 10
        obstacle = next(iter(self.game.obstacles))
        self.assertFalse(self.game.check_collision(obstacle))

    def test_obstacles_start_empty(self):
        self.game.score = 0
        self.game.generate_obstacles()
        self.assertEqual(len(self.game.obstacles), 0)

    def test_obstacles_appear_after_score_threshold(self):
        self.game.score = 6
        self.game.generate_obstacles()
        self.assertGreater(len(self.game.obstacles), 0)

    def test_losing_life_reduces_lives_by_one(self):
        self.game.lives = 3
        self.game.snake = [(10, 10), (9, 10), (8, 10), (7, 10)]
        self.game.lose_life()
        self.assertEqual(self.game.lives, 2)

    def test_snake_length_carries_over_after_losing_life(self):
        self.game.lives = 3
        self.game.snake = [(10, 10), (9, 10), (8, 10), (7, 10), (6, 10), (5, 10)]
        original_length = len(self.game.snake)

        self.game.lose_life()

        self.assertEqual(self.game.lives, 2)
        self.assertEqual(len(self.game.snake), original_length)

    def test_game_ends_when_lives_reach_zero(self):
        self.game.lives = 1
        self.game.lose_life()
        self.assertTrue(self.game.game_over)

    def test_high_score_updates(self):
        self.game.score = 5
        self.game.high_score = 4
        self.game.food_type = "normal"
        self.game.handle_food_effect()
        self.assertEqual(self.game.high_score, 6)

    def test_speed_increases_as_score_increases(self):
        self.game.score = 0
        self.game.update_base_speed()
        start_speed = self.game.base_speed

        self.game.score = 10
        self.game.update_base_speed()
        faster_speed = self.game.base_speed

        self.assertLess(faster_speed, start_speed)

    def test_spawn_food_does_not_place_food_on_snake(self):
        self.game.snake = [(5, 5), (4, 5), (3, 5)]
        self.game.score = 6
        self.game.generate_obstacles()

        for _ in range(25):
            self.game.spawn_food()
            self.assertNotIn(self.game.food, self.game.snake)
            self.assertNotIn(self.game.food, self.game.obstacles)


if __name__ == "__main__":
    unittest.main()