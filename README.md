# Snake Game Deluxe

## Project Overview

Snake Game Deluxe is a Python arcade-style game built using the `tkinter` library. The player controls a snake that moves across the screen, collects food, grows longer, and tries to survive as long as possible without colliding with the walls, obstacles, or its own body.

This version expands on the classic snake game by adding multiple food types, power ups, a three-life system, gradually appearing obstacles, and smooth speed progression as the game continues. The goal of the project was to create a game that is fun, visually clear, and more unique than a basic snake implementation while still being simple enough to run with standard Python tools.

The game is fully compatible with Python 3.12.5 and uses only built in Python libraries, so no extra installation is required beyond having Python installed.

---

## Features

### Core Gameplay
- Classic snake movement using the arrow keys
- Snake grows as food is collected
- Score increases as the player survives and eats food
- Game ends after all three lives are lost

### Unique Features Added
- **Three-life system** instead of immediate game over after one crash
- **Snake length carries over** between lives until all lives are lost
- **Gradually increasing speed** as the score gets higher
- **Obstacles that appear over time** instead of being present at the start
- **Power up foods** with different effects
- **Pause and restart controls**
- **Main menu food key** explaining what each colored food does
- **High score tracking during the session**

---

## Food Types

The game contains four different food types, each identified by color.

### Red Food
- Standard food
- Adds **1 point**

### Gold Food
- Bonus food
- Adds **3 points**

### Blue Food
- Slow power up
- Adds **1 point**
- Temporarily slows the snake

### Purple Food
- Ghost power up
- Adds **1 point**
- Temporarily allows the snake to pass through obstacles

---

## How the Game Works

At the beginning of the game, the player starts with:
- 3 lives
- a short snake
- no obstacles on the board

As the player eats more food:
- the snake becomes longer
- the score increases
- the snake speed increases gradually
- obstacle groups begin appearing at higher score thresholds

If the snake crashes into:
- the wall
- its own body
- an obstacle while ghost mode is not active

then the player loses one life.

If the player still has lives remaining:
- the snake respawns
- the score remains the same
- the snake keeps its length from the previous life

If all three lives are lost:
- the game ends
- the player can restart by pressing `R` or using the Restart button

---

## Controls

- **Up Arrow** → move up
- **Down Arrow** → move down
- **Left Arrow** → move left
- **Right Arrow** → move right
- **P** → pause or resume the game
- **R** → restart the full game

There are also on-screen buttons for:
- Restart
- Pause / Resume
- Exit

---

## Libraries Used

This project uses only built in Python libraries:

- `tkinter` for the graphical user interface
- `random` for generating food locations and food types

Because only built in libraries are used, this project does not require `pip install` commands or any external packages.

---

## Compatibility

This project was designed to run with:

- **Python 3.12.5**

It should also work with most recent Python 3 versions that include `tkinter`.

---

## How to Run the Program

1. Make sure Python is installed on your computer.
2. Save the game code in a file named:

```python
snake_game.py