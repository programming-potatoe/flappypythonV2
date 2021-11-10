import pygame
import enum

# all of my important constants

# GAME CONSTANTS
class Gamemodes(enum.Enum):
    startscreen = 1
    running = 2
    lostscreen = 3
    exit = 4

# WINDOW CONSTANTS
WIDTH, HEIGHT = 2000, 1500
CAPTION = "FlappyPythonV2"
FPS = 60
HIGHSCORE_FONT = pygame.font.SysFont("comicsans", 50)
LOOSE_FONT = pygame.font.SysFont("comicsans", 200)

# COLORS
RED = (255,0,0)
GREEN = (0,255,0)

# BIRD CONSTANTS
BIRD_WIDTH, BIRD_HEIGHT = 125,125
BIRD_SPAWN = (BIRD_WIDTH/2 + 50, HEIGHT/2)
BIRD_INITIAL_STEP_SIZE = 5
BIRD_MAX_ROTATION_DOWN = 40
BIRD_MAX_ROTATION_UP = 20

# PIPE CONSTANTS
PIPE_WIDHT = 200
PIPE_HOLE_SIZE = 200
PIPE_SPAWN_TIMER = 4
PIPE_SPEED = 40
PIPE_UPPER = 0
PIPE_LOWER = 1

# CUSTOM EVENTS
GAME_LOST = pygame.USEREVENT + 1
HIGHSCORE_NEW_PONIT = pygame.USEREVENT + 2
PIPE_SPAWN = pygame.USEREVENT + 3