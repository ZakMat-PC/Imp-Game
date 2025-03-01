import pygame
import random
import os
import sqlite3

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600 
IMP_WIDTH = 40
IMP_HEIGHT = 30
PILLAR_WIDTH = 60
PILLAR_GAP = 150
GRAVITY = 0.6
FLAP_STRENGTH = -9
PILLAR_SPEED = 5  # Speed for pillars

# Colors
WHITE = (255, 255, 255)

# Path to the SQLite database
BASE_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(BASE_DIR, 'high_scores.db')

def init_db():
    """Initialize the SQLite database and create the high_scores table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def load_high_score():
    """Load the high score from the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(score) FROM high_scores')
    high_score = cursor.fetchone()[0]
    conn.close()
    return high_score if high_score is not None else 0

def save_high_score(score):
    """Save the high score to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM high_scores')  # Remove old scores
    cursor.execute('INSERT INTO high_scores (score) VALUES (?)', (score,))
    conn.commit()
    conn.close()
    print(f"Saved high score: {score}")  # Debug statement

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Imp")

# Define the path to the assets directory
assets_dir = os.path.join(BASE_DIR, 'assets')

# Load images using relative paths
background_image = pygame.image.load(os.path.join(assets_dir, 'background.png'))
pillar_image = pygame.image.load(os.path.join(assets_dir, 'pillar.png'))

# Scale images to fit the game
pillar_image = pygame.transform.scale(pillar_image, (PILLAR_WIDTH, SCREEN_HEIGHT))

# Load imp frames
imp_frames = []
for i in range(1, 5):  # Assuming you have 4 frames named imp_frame_1.png, imp_frame_2.png, etc.
    frame = pygame.image.load(os.path.join(assets_dir, f'imp_frame_{i}.png'))
    frame = pygame.transform.scale(frame, (IMP_WIDTH, IMP_HEIGHT))
    imp_frames.append(frame)

# Imp class
class Imp:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.frame_index = 0
        self.frame_counter = 0

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Update animation frame
        self.frame_counter += 1
        if self.frame_counter % 5 == 0:  # Change frame every 5 ticks
            self.frame_index = (self.frame_index + 1) % len(imp_frames)
        self.frame_counter %= 30  # Reset counter after 30 ticks (adjust speed as needed)

        # Check for boundary conditions
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y + IMP_HEIGHT > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - IMP_HEIGHT
            self.velocity = 0

    def flap(self):
        # Flap upward
        self.velocity = FLAP_STRENGTH

    def draw(self):
        screen.blit(imp_frames[self.frame_index], (self.x, self.y))

# Pillar class
class Pillar:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PILLAR_GAP - 100)
        self.speed = PILLAR_SPEED  # Speed for pillars
    
    def update(self):
        # Move the pillar to the left
        self.x -= self.speed

    def draw(self):
        # Draw the top pillar (flipped vertically)
        top_pillar = pygame.transform.flip(pillar_image, False, True)  # Flip the image vertically
        screen.blit(top_pillar, (self.x, 0), (0, pillar_image.get_height() - self.height, PILLAR_WIDTH, self.height))  # Top pillar
        
        # Draw the bottom pillar (normal position)
        screen.blit(pillar_image, (self.x, self.height + PILLAR_GAP), (0, 0, PILLAR_WIDTH, pillar_image.get_height()))

    def is_off_screen(self):
        return self.x + PILLAR_WIDTH < 0

    def has_collided(self, imp):
        # Check collision with imp
        if imp.x + IMP_WIDTH > self.x and imp.x < self.x + PILLAR_WIDTH:
            if imp.y < self.height or imp.y + IMP_HEIGHT > self.height + PILLAR_GAP:
                return True
        return False

# Start menu function
def start_menu(high_score):
    font = pygame.font.SysFont(None, 48)
    title_text = font.render("Imp", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    exit_text = font.render("Press ESC to Exit", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    
    while True:
        draw_background()  # Draw background
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

# Game over screen function
def game_over_screen(score):
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    replay_text = font.render("Press R to Replay", True, WHITE)
    exit_text = font.render("Press ESC to Exit", True, WHITE)
    
    while True:
        draw_background()  # Draw background
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(replay_text, (SCREEN_WIDTH // 2 - replay_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "replay"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

# Modified function to draw a static background
def draw_background():
    # Draw a static background
    screen.blit(background_image, (0, 0))  # Draw the background once, no movement

# Main game loop
def main():
    # Initialize the database at the start
    init_db()
    
    # Load the high score
    high_score = load_high_score()

    while True:
        start_menu(high_score)  # Show the start menu with high score

        # Create an imp instance
        imp = Imp()

        # Create a list to hold pillars
        pillars = [Pillar()]

        # Set up the clock for controlling frame rate
        clock = pygame.time.Clock()

        # Game variables
        score = 0
        game_over = False

        while not game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        imp.flap()

            # Update imp
            imp.update()

            # Update pillars
            for pillar in pillars:
                pillar.update()

            # Add new pillars
            if pillars[-1].x < SCREEN_WIDTH - 300:
                pillars.append(Pillar())

            # Remove off-screen pillars
            pillars = [pillar for pillar in pillars if not pillar.is_off_screen()]

            # Check for collisions with pillars
            for pillar in pillars:
                if pillar.has_collided(imp):
                    game_over = True

            # Check if the imp hits the ground or flies off the screen
            if imp.y + IMP_HEIGHT > SCREEN_HEIGHT or imp.y < 0:
                game_over = True

            # Increase score if the imp passes a pillar
            if pillars[0].x + PILLAR_WIDTH < imp.x and not game_over:
                score += 1

            # Drawing section
            draw_background()  # Draw the static background
            imp.draw()
            for pillar in pillars:
                pillar.draw()
            
            # Draw score
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)

        # Update high score if necessary
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        # Show the game over screen
        result = game_over_screen(score)
        if result == "replay":
            continue  # Restart the game
        else:
            pygame.quit()
            quit()

# Run the game
if __name__ == "__main__":
    main()
