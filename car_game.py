import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 30

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Crazy Car Game')

# Load and set the icon for the game window
icon = pygame.image.load('Car_icon.jpg')
pygame.display.set_icon(icon)

# Load the road picture
road = pygame.image.load('road_0.png')
road_width, road_height = road.get_width(), road.get_height()
road_y = 0  # Start at the top of the screen

# Car properties
car_width, car_height = 300, 280
car_x = (SCREEN_WIDTH - car_width) // 2
car_y = SCREEN_HEIGHT - car_height - 20
car_speed = 45

# Hurdle properties
hurdle_width, hurdle_height = 50, 50
hurdle_speed = 5

# Initialize score and font
score = 0
font = pygame.font.Font(None, 36)

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('car.png'), (car_width, car_height))
        self.rect = self.image.get_rect()
        self.rect.x = car_x
        self.rect.y = car_y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x = max(0, self.rect.x - car_speed)
        if keys[pygame.K_RIGHT]:
            self.rect.x = min(SCREEN_WIDTH - car_width, self.rect.x + car_speed)
        if keys[pygame.K_UP]:
            self.rect.y = max(0, self.rect.y - car_speed)
        if keys[pygame.K_DOWN]:
            self.rect.y = min(SCREEN_HEIGHT - car_height, self.rect.y + car_speed)

class Hurdle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((hurdle_width, hurdle_height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - hurdle_width)
        self.rect.y = -hurdle_height

    def update(self):
        self.rect.y += hurdle_speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            global score
            score += 1

car_sprite = pygame.sprite.GroupSingle(Car())
hurdle_group = pygame.sprite.Group()

# Display score
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Display game over screen
def display_game_over():
    game_over_text = font.render("Game Over! Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

class GameState:
    PLAYING = 0
    GAME_OVER = 1

current_state = GameState.PLAYING

def main_game_loop():
    global road_y, current_state

    while current_state == GameState.PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Update game objects
        car_sprite.update()
        hurdle_group.update()

        # Spawn new hurdles
        if random.randint(1, 100) == 1:
            hurdle_group.add(Hurdle())

        # Check for collisions
        if pygame.sprite.spritecollide(car_sprite.sprite, hurdle_group, False):
            current_state = GameState.GAME_OVER

        # Update road position
        road_y += 5
        if road_y >= road_height:
            road_y = 0

        # Draw everything
        screen.blit(road, (0, road_y))
        screen.blit(road, (0, road_y - road_height))
        car_sprite.draw(screen)
        hurdle_group.draw(screen)
        display_score()

        pygame.display.flip()
        clock.tick(FPS)

    return True

def game_over_loop():
    global current_state, score

    while current_state == GameState.GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    current_state = GameState.PLAYING
                    car_sprite.sprite.rect.x = car_x
                    car_sprite.sprite.rect.y = car_y
                    hurdle_group.empty()
                    score = 0
                    return True
                if event.key == pygame.K_q:
                    return False

        screen.fill(BLACK)
        display_game_over()
        pygame.display.flip()
        clock.tick(FPS)

    return True

# Main game loop
clock = pygame.time.Clock()

while True:
    if not main_game_loop() or not game_over_loop():
        break

pygame.quit()
sys.exit()