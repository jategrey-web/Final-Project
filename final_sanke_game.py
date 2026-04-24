import tkinter as tk
import random

# ==========================================================
# Snake Game Deluxe
# Python 3.12.5 compatible
#
# Controls:
#   Arrow keys = move
#   P = pause
#   R = restart game
#
# Features:
#   - 3 lives system
#   - Obstacles appear gradually as score increases
#   - Smooth speed increase as game continues
#   - Snake keeps its length after losing a life
#   - Power ups
#   - Main menu food key
# ==========================================================

WINDOW_BG = "#e8edf2"
BOARD_WIDTH = 600
BOARD_HEIGHT = 600
CELL_SIZE = 24

GRID_WIDTH = BOARD_WIDTH // CELL_SIZE
GRID_HEIGHT = BOARD_HEIGHT // CELL_SIZE

INITIAL_SPEED = 150
MIN_SPEED = 65
SPEED_STEP = 2

POWER_UP_DURATION = 40

OBSTACLE_LAYOUT = [
    [(8, y) for y in range(6, 19)],
    [(x, 10) for x in range(14, 21)],
    [(18, y) for y in range(4, 9)],
    [(x, 18) for x in range(4, 9)],
]

OBSTACLE_THRESHOLDS = [6, 12, 18, 24]


class StartScreen:
    def __init__(self, root, start_callback):
        self.root = root
        self.start_callback = start_callback

        self.frame = tk.Frame(root, bg=WINDOW_BG, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame,
            text="Snake Game Deluxe",
            font=("Arial", 28, "bold"),
            bg=WINDOW_BG,
            fg="#233142",
        ).pack(pady=(30, 10))

        tk.Label(
            self.frame,
            text="Now with obstacles, power ups, and 3 lives",
            font=("Arial", 13),
            bg=WINDOW_BG,
            fg="#3f5364",
        ).pack(pady=(0, 20))

        instructions = (
            "Goal:\n"
            "Eat food, grow longer, and survive as long as possible.\n"
            "You have 3 lives total.\n\n"
            "Controls:\n"
            "Arrow keys = move\n"
            "P = pause\n"
            "R = restart game"
        )

        tk.Label(
            self.frame,
            text=instructions,
            font=("Arial", 12),
            justify="center",
            bg=WINDOW_BG,
            fg="#2e3d49",
        ).pack(pady=8)

        key_frame = tk.Frame(self.frame, bg="white", bd=1, relief="solid", padx=16, pady=12)
        key_frame.pack(pady=18)

        tk.Label(
            key_frame,
            text="Food Key",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#233142",
        ).pack(pady=(0, 10))

        self.make_key_row(key_frame, "#d94f70", "Red", "Normal food: +1 point")
        self.make_key_row(key_frame, "#f0c419", "Gold", "Bonus food: +3 points")
        self.make_key_row(key_frame, "#4aa3ff", "Blue", "Slow food: slows the snake briefly")
        self.make_key_row(key_frame, "#9b6bff", "Purple", "Ghost food: lets you pass through obstacles briefly")

        tk.Button(
            self.frame,
            text="Start Game",
            font=("Arial", 14, "bold"),
            width=14,
            command=self.start_game,
            bg="#4f9d69",
            fg="white",
            activebackground="#3d8454",
        ).pack(pady=20)

        tk.Button(
            self.frame,
            text="Exit",
            font=("Arial", 12),
            width=10,
            command=root.destroy,
            bg="#b85042",
            fg="white",
            activebackground="#953c31",
        ).pack(pady=5)

    def make_key_row(self, parent, color, label_text, description):
        row = tk.Frame(parent, bg="white")
        row.pack(anchor="w", pady=4)

        swatch = tk.Canvas(row, width=18, height=18, bg="white", highlightthickness=0)
        swatch.pack(side="left", padx=(0, 8))
        swatch.create_oval(2, 2, 16, 16, fill=color, outline="black")

        tk.Label(
            row,
            text=f"{label_text}: {description}",
            font=("Arial", 11),
            bg="white",
            fg="#2e3d49",
            anchor="w",
            justify="left",
        ).pack(side="left")

    def start_game(self):
        self.frame.destroy()
        self.start_callback()


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game Deluxe")
        self.root.configure(bg=WINDOW_BG)

        self.after_id = None
        self.high_score = 0

        self.main_frame = tk.Frame(root, bg=WINDOW_BG, padx=10, pady=10)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame,
            text="Snake Game Deluxe",
            font=("Arial", 20, "bold"),
            bg=WINDOW_BG,
            fg="#233142",
        ).pack(pady=(0, 8))

        self.status_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 11, "bold"),
            bg=WINDOW_BG,
            fg="#2e3d49",
        )
        self.status_label.pack(pady=(0, 8))

        self.canvas = tk.Canvas(
            self.main_frame,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg="#f7f4ea",
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(pady=5)

        controls = tk.Frame(self.main_frame, bg=WINDOW_BG)
        controls.pack(pady=10)

        tk.Button(
            controls, text="Restart", width=12,
            command=self.restart_game, bg="#7c8da6", fg="white"
        ).grid(row=0, column=0, padx=4, pady=4)

        tk.Button(
            controls, text="Pause / Resume", width=12,
            command=self.toggle_pause, bg="#567189", fg="white"
        ).grid(row=0, column=1, padx=4, pady=4)

        tk.Button(
            controls, text="Exit", width=12,
            command=self.root.destroy, bg="#b85042", fg="white"
        ).grid(row=0, column=2, padx=4, pady=4)

        tk.Label(
            self.main_frame,
            text="Arrow keys: move    P: pause    R: restart game",
            font=("Arial", 10),
            bg=WINDOW_BG,
            fg="#4d5d6b",
        ).pack(pady=(0, 6))

        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("p", lambda event: self.toggle_pause())
        self.root.bind("P", lambda event: self.toggle_pause())
        self.root.bind("r", lambda event: self.restart_game())
        self.root.bind("R", lambda event: self.restart_game())

        self.setup_full_game()
        self.draw()
        self.game_loop()

    def setup_full_game(self):
        self.score = 0
        self.lives = 3
        self.food = None
        self.food_type = "normal"
        self.slow_timer = 0
        self.ghost_timer = 0
        self.paused = False
        self.game_over = False

        self.saved_length = 3
        self.start_round(reset_length=True)

    def start_round(self, reset_length=False):
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2

        if reset_length:
            self.saved_length = 3

        length = max(3, self.saved_length)

        # Start horizontally from center
        self.snake = []
        for i in range(length):
            self.snake.append((center_x - i, center_y))

        self.direction = "Right"
        self.next_direction = "Right"

        self.slow_timer = 0
        self.ghost_timer = 0
        self.paused = False
        self.game_over = False

        self.update_base_speed()
        self.generate_obstacles()
        self.spawn_food()

    def restart_game(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.setup_full_game()
        self.draw()
        self.game_loop()

    def toggle_pause(self):
        if self.game_over:
            return
        self.paused = not self.paused
        self.draw()
        if not self.paused:
            self.game_loop()

    def update_base_speed(self):
        self.base_speed = max(MIN_SPEED, INITIAL_SPEED - self.score * SPEED_STEP)
        if self.slow_timer > 0:
            self.speed = min(self.base_speed + 45, INITIAL_SPEED + 40)
        else:
            self.speed = self.base_speed

    def generate_obstacles(self):
        self.obstacles = set()

        for threshold, group in zip(OBSTACLE_THRESHOLDS, OBSTACLE_LAYOUT):
            if self.score >= threshold:
                self.obstacles.update(group)

        self.obstacles = {
            pos for pos in self.obstacles
            if pos not in self.snake
        }

    def spawn_food(self):
        roll = random.random()
        if roll < 0.12:
            self.food_type = "bonus"
        elif roll < 0.20:
            self.food_type = "slow"
        elif roll < 0.27:
            self.food_type = "ghost"
        else:
            self.food_type = "normal"

        while True:
            position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if position not in self.snake and position not in self.obstacles:
                self.food = position
                return

    def change_direction(self, new_direction):
        opposite = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left",
        }
        if len(self.snake) > 1 and new_direction == opposite[self.direction]:
            return
        self.next_direction = new_direction

    def move_snake(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)

        if self.check_collision(new_head):
            self.lose_life()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.handle_food_effect()
            self.saved_length = len(self.snake)
            self.generate_obstacles()
            self.spawn_food()
        else:
            self.snake.pop()
            self.saved_length = len(self.snake)

        self.update_powerups()

    def handle_food_effect(self):
        if self.food_type == "normal":
            self.score += 1
        elif self.food_type == "bonus":
            self.score += 3
        elif self.food_type == "slow":
            self.score += 1
            self.slow_timer = POWER_UP_DURATION
        elif self.food_type == "ghost":
            self.score += 1
            self.ghost_timer = POWER_UP_DURATION

        if self.score > self.high_score:
            self.high_score = self.score

        self.update_base_speed()

    def update_powerups(self):
        if self.slow_timer > 0:
            self.slow_timer -= 1

        if self.ghost_timer > 0:
            self.ghost_timer -= 1

        self.update_base_speed()

    def check_collision(self, position):
        x, y = position

        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True

        if position in self.snake:
            return True

        if position in self.obstacles and self.ghost_timer == 0:
            return True

        return False

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.end_game()
            return

        # Keep current length into the next life
        self.saved_length = max(3, len(self.snake))
        self.start_round(reset_length=False)
        self.draw()

    def draw_grid(self):
        for x in range(0, BOARD_WIDTH, CELL_SIZE):
            self.canvas.create_line(x, 0, x, BOARD_HEIGHT, fill="#e3ddd0")
        for y in range(0, BOARD_HEIGHT, CELL_SIZE):
            self.canvas.create_line(0, y, BOARD_WIDTH, y, fill="#e3ddd0")

    def draw_obstacles(self):
        for x, y in self.obstacles:
            left = x * CELL_SIZE
            top = y * CELL_SIZE
            right = left + CELL_SIZE
            bottom = top + CELL_SIZE
            self.canvas.create_rectangle(
                left + 2, top + 2, right - 2, bottom - 2,
                fill="#555555", outline="#2e2e2e", width=2
            )

    def draw_snake(self):
        for index, (x, y) in enumerate(self.snake):
            left = x * CELL_SIZE
            top = y * CELL_SIZE
            right = left + CELL_SIZE
            bottom = top + CELL_SIZE

            if self.ghost_timer > 0:
                body_color = "#9b6bff"
                outline = "#5f36b3"
                head_color = "#7f4cff"
            else:
                body_color = "#4f9d69"
                outline = "#2f6d46"
                head_color = "#2f7d32"

            fill_color = head_color if index == 0 else body_color

            self.canvas.create_rectangle(
                left + 2, top + 2, right - 2, bottom - 2,
                fill=fill_color, outline=outline, width=2
            )

        head_x, head_y = self.snake[0]
        left = head_x * CELL_SIZE
        top = head_y * CELL_SIZE
        self.canvas.create_oval(left + 6, top + 6, left + 9, top + 9, fill="white", outline="")
        self.canvas.create_oval(left + 15, top + 6, left + 18, top + 9, fill="white", outline="")

    def draw_food(self):
        x, y = self.food
        left = x * CELL_SIZE
        top = y * CELL_SIZE
        right = left + CELL_SIZE
        bottom = top + CELL_SIZE

        if self.food_type == "normal":
            fill = "#d94f70"
            outline = "#8c213c"
        elif self.food_type == "bonus":
            fill = "#f0c419"
            outline = "#a57f00"
        elif self.food_type == "slow":
            fill = "#4aa3ff"
            outline = "#1f5f99"
        else:
            fill = "#9b6bff"
            outline = "#5f36b3"

        self.canvas.create_oval(
            left + 4, top + 4, right - 4, bottom - 4,
            fill=fill, outline=outline, width=2
        )

    def draw_overlay_text(self, title, subtitle=""):
        self.canvas.create_rectangle(
            90, 220, BOARD_WIDTH - 90, BOARD_HEIGHT - 220,
            fill="#ffffff", outline="#9aa7b2", width=2
        )
        self.canvas.create_text(
            BOARD_WIDTH // 2, BOARD_HEIGHT // 2 - 18,
            text=title, font=("Arial", 24, "bold"), fill="#233142"
        )
        if subtitle:
            self.canvas.create_text(
                BOARD_WIDTH // 2, BOARD_HEIGHT // 2 + 20,
                text=subtitle, font=("Arial", 12), fill="#3f5364"
            )

    def draw(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_obstacles()
        self.draw_food()
        self.draw_snake()

        effects = []
        if self.slow_timer > 0:
            effects.append(f"Slow: {self.slow_timer}")
        if self.ghost_timer > 0:
            effects.append(f"Ghost: {self.ghost_timer}")
        effect_text = " | ".join(effects) if effects else "None"

        self.status_label.config(
            text=(
                f"Score: {self.score}    "
                f"High Score: {self.high_score}    "
                f"Lives: {self.lives}    "
                f"Length: {len(self.snake)}    "
                f"Effects: {effect_text}"
            )
        )

        if self.paused and not self.game_over:
            self.draw_overlay_text("Paused", "Press P to continue")

        if self.game_over:
            self.draw_overlay_text("Game Over", "Press R to restart the full game")

    def end_game(self):
        self.game_over = True
        self.draw()

    def game_loop(self):
        if self.game_over:
            self.draw()
            return

        if not self.paused:
            self.move_snake()
            self.draw()

        self.after_id = self.root.after(self.speed, self.game_loop)


def main():
    root = tk.Tk()
    root.title("Snake Game Deluxe")
    root.configure(bg=WINDOW_BG)
    root.resizable(False, False)

    def launch_game():
        SnakeGame(root)

    StartScreen(root, launch_game)
    root.mainloop()


if __name__ == "__main__":
    main()