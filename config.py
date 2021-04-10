import pygame

CHAR_WIDTH = 20
PELLETS    = 191
X          = 520 + CHAR_WIDTH
Y          = 620 + CHAR_WIDTH

GREEN = (90, 197, 92)
YELLOW = (252, 241, 16)
WHITE = (255, 255, 255)

# Indexes
NORMAL_PELLET     = 0
WALL              = 1
RESTRICTED        = 2
BLANK             = 3
POWER_EAT         = 4
POWER             = 5
NORMAL_PELLET_EAT = 6
GHOST_BARRIER     = 7

# STAGES
SCATTER = 1
CHASE   = 2

# Faces
STILL  = 0
LEFT  = 1
RIGHT = 2
UP    = 3
DOWN  = 4

# Modes
NORMAL     = 0
FRIGHTENED = 1

digit_font = "assets/fonts/DS-DIGIB.TTF"

death_sprites = [
  pygame.image.load('assets/sprites/die_1.png'),
  pygame.image.load('assets/sprites/die_2.png'),
  pygame.image.load('assets/sprites/die_3.png'),
  pygame.image.load('assets/sprites/die_4.png'),
  pygame.image.load('assets/sprites/die_5.png'),
  pygame.image.load('assets/sprites/die_6.png'),
  pygame.image.load('assets/sprites/die_7.png'),
  pygame.image.load('assets/sprites/die_8.png'),
  pygame.image.load('assets/sprites/die_9.png'),
  pygame.image.load('assets/sprites/die_10.png'),
  pygame.image.load('assets/sprites/die_11.png')
]

frightened_ghost = pygame.image.load("assets/sprites/run.png")
frightened_ghost_over = pygame.image.load("assets/sprites/run_over.png")
ghost_dead_sprites = [frightened_ghost, frightened_ghost_over]

maze = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
  [1, 5, 1, 2, 2, 1, 0, 1, 2, 2, 2, 1, 0, 1, 0, 1, 2, 2, 2, 1, 0, 1, 2, 2, 1, 5, 1],
  [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 1, 1, 1, 0, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 0, 1, 1, 1, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 1],
  [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
  [1, 2, 2, 2, 2, 1, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 1, 2, 2, 2, 2, 1],
  [1, 2, 2, 2, 2, 1, 0, 1, 3, 1, 1, 1, 7, 7, 7, 1, 1, 1, 3, 1, 0, 1, 2, 2, 2, 2, 1],
  [1, 1, 1, 1, 1, 1, 0, 1, 3, 1, 2, 2, 2, 2, 2, 2, 2, 1, 3, 1, 0, 1, 1, 1, 1, 1, 1],
  [3, 3, 3, 3, 3, 3, 0, 3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 1, 3, 3, 0, 3, 3, 3, 3, 3, 3],
  [1, 1, 1, 1, 1, 1, 0, 1, 3, 1, 2, 2, 2, 2, 2, 2, 2, 1, 3, 1, 0, 1, 1, 1, 1, 1, 1],
  [1, 2, 2, 2, 2, 1, 0, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 0, 1, 2, 2, 2, 2, 1],
  [1, 2, 2, 2, 2, 1, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 1, 2, 2, 2, 2, 1],
  [1, 1, 1, 1, 1, 1, 0, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 0, 1, 1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
  [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 1],
  [1, 1, 1, 1, 3, 1, 3, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 3, 1, 3, 1, 1, 1, 1],
  [1, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 5, 1, 5, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 1],
  [1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1],
  [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

characters = {
  "pacman": {
    "id": 1,
    "theme": (244, 240, 33),
    "coordinates": (260, 300),
    "sprites": [pygame.image.load('assets/sprites/still.png'), pygame.image.load('assets/sprites/left_c.png'), pygame.image.load('assets/sprites/right_c.png'), pygame.image.load('assets/sprites/up_c.png'), pygame.image.load('assets/sprites/down_c.png')],
    "walkRight": [pygame.image.load('assets/sprites/right_c.png'), pygame.image.load('assets/sprites/right_o.png')],
    "walkLeft": [pygame.image.load('assets/sprites/left_c.png'), pygame.image.load('assets/sprites/left_o.png')],
    "walkUp": [pygame.image.load('assets/sprites/up_c.png'), pygame.image.load('assets/sprites/up_o.png')],
    "walkDown": [pygame.image.load('assets/sprites/down_c.png'), pygame.image.load('assets/sprites/down_o.png')]
  },
  "blinky": {
    "id": 2,
    "theme": (239, 72, 50),
    "coordinates": (260, 180),
    "sprites": [pygame.image.load('assets/sprites/blinky_still.png'), pygame.image.load('assets/sprites/blinky_left.png'), pygame.image.load('assets/sprites/blinky_right.png'), pygame.image.load('assets/sprites/blinky_up.png'), pygame.image.load('assets/sprites/blinky_down.png')],
    "scatterLocation": (500, 20),
    "walkRight": [pygame.image.load('assets/sprites/blinky_right.png'), pygame.image.load('assets/sprites/blinky_right.png')],
    "walkLeft": [pygame.image.load('assets/sprites/blinky_left.png'), pygame.image.load('assets/sprites/blinky_left.png')],
    "walkUp": [pygame.image.load('assets/sprites/blinky_up.png'), pygame.image.load('assets/sprites/blinky_up.png')],
    "walkDown": [pygame.image.load('assets/sprites/blinky_down.png'), pygame.image.load('assets/sprites/blinky_down.png')]
  },
  "pinky": {
    "id": 3,
    "theme": (240, 157, 251),
    "coordinates": (240, 220),
    "sprites": [pygame.image.load('assets/sprites/pinky_still.png'), pygame.image.load('assets/sprites/pinky_left.png'), pygame.image.load('assets/sprites/pinky_right.png'), pygame.image.load('assets/sprites/pinky_up.png'), pygame.image.load('assets/sprites/pinky_down.png')],
    "scatterLocation": (20, 20),
    "walkRight": [pygame.image.load('assets/sprites/pinky_right.png'), pygame.image.load('assets/sprites/pinky_right.png')],
    "walkLeft": [pygame.image.load('assets/sprites/pinky_left.png'), pygame.image.load('assets/sprites/pinky_left.png')],
    "walkUp": [pygame.image.load('assets/sprites/pinky_up.png'), pygame.image.load('assets/sprites/pinky_up.png')],
    "walkDown": [pygame.image.load('assets/sprites/pinky_down.png'), pygame.image.load('assets/sprites/pinky_down.png')]
  },
  "inky": {
    "id": 4,
    "theme": (101, 239, 233),
    "coordinates": (260, 220),
    "sprites": [pygame.image.load('assets/sprites/inky_still.png'), pygame.image.load('assets/sprites/inky_left.png'), pygame.image.load('assets/sprites/inky_right.png'), pygame.image.load('assets/sprites/inky_up.png'), pygame.image.load('assets/sprites/inky_down.png')],
    "scatterLocation": (500, 460),
    "walkRight": [pygame.image.load('assets/sprites/inky_right.png'), pygame.image.load('assets/sprites/inky_right.png')],
    "walkLeft": [pygame.image.load('assets/sprites/inky_left.png'), pygame.image.load('assets/sprites/inky_left.png')],
    "walkUp": [pygame.image.load('assets/sprites/inky_up.png'), pygame.image.load('assets/sprites/inky_up.png')],
    "walkDown": [pygame.image.load('assets/sprites/inky_down.png'), pygame.image.load('assets/sprites/inky_down.png')]
  },
  "clyde": {
    "id": 5,
    "theme": (248, 184, 71),
    "coordinates": (280, 220),
    "sprites": [pygame.image.load('assets/sprites/clyde_still.png'), pygame.image.load('assets/sprites/clyde_left.png'), pygame.image.load('assets/sprites/clyde_right.png'), pygame.image.load('assets/sprites/clyde_up.png'), pygame.image.load('assets/sprites/clyde_down.png')],
    "scatterLocation": (20, 460),
    "walkRight": [pygame.image.load('assets/sprites/clyde_right.png'), pygame.image.load('assets/sprites/clyde_right.png')],
    "walkLeft": [pygame.image.load('assets/sprites/clyde_left.png'), pygame.image.load('assets/sprites/clyde_left.png')],
    "walkUp": [pygame.image.load('assets/sprites/clyde_up.png'), pygame.image.load('assets/sprites/clyde_up.png')],
    "walkDown": [pygame.image.load('assets/sprites/clyde_down.png'), pygame.image.load('assets/sprites/clyde_down.png')]
  }
}
