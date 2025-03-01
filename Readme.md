# Imp - A Flappy Bird Clone

## Overview
Imp is a simple Flappy Bird-style game built using Python and Pygame. The game features an animated imp character, procedurally generated pillars, and a local high-score tracking system using SQLite.

## Features
- Smooth animation with multiple frames for the imp.
- Gravity and flap mechanics for a responsive feel.
- Randomly generated obstacles for endless gameplay.
- Local high score tracking using an SQLite database.
- Start menu and game-over screen with replay functionality.

## Installation
### Prerequisites
Ensure you have Python installed (preferably Python 3.7+). You can download it from [python.org](https://www.python.org/downloads/).

### Install Dependencies
Run the following command to install the required dependencies:
```sh
pip install -r requirements.txt

How to Play
Press SPACE to start the game and flap the imp's wings.
Navigate through the gaps between pillars.
Avoid crashing into the pillars or the ground.
Your score increases as you pass through pillars.
The highest score is stored in an SQLite database.
Controls
SPACE: Flap the imp upwards
ESC: Exit the game
R: Restart after game over
Running the Game
Execute the following command in the terminal:
main.py
