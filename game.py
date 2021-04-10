from config import (
  maze,
  characters, death_sprites, ghost_dead_sprites,
  X, Y, CHAR_WIDTH,
  PELLETS,
  digit_font,
  NORMAL_PELLET, WALL, RESTRICTED, BLANK, POWER_EAT, POWER, NORMAL_PELLET_EAT, GHOST_BARRIER,
  STILL, LEFT, RIGHT, UP, DOWN,
  SCATTER, CHASE,
  NORMAL, FRIGHTENED,
  GREEN, YELLOW, WHITE
)
from pygame.constants import KEYDOWN, K_SPACE, MOUSEBUTTONDOWN
from pygame.font import Font
import threading, sys, os, pickle
from math import sqrt
import pygame

# --------- Load pygame config --------- 
pygame.init()
pygame.display.set_caption("PACMAN")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

# --------- Load background --------- 
bg    = pygame.image.load("assets/background.jpg")
win   = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()

# --------- Sound Effects & Background Music --------- 
filePath = 'assets/sounds'
chomp     = pygame.mixer.Sound(os.path.join(filePath, 'chomp.ogg'))
death     = pygame.mixer.Sound(os.path.join(filePath, 'death.ogg'))
bonus     = pygame.mixer.Sound(os.path.join(filePath, 'bonus.ogg'))
go        = pygame.mixer.Sound(os.path.join(filePath, 'go.ogg'))
gameover  = pygame.mixer.Sound(os.path.join(filePath, 'gameover.ogg'))
count     = pygame.mixer.Sound(os.path.join(filePath, 'count.ogg'))
eatGhost  = pygame.mixer.Sound(os.path.join(filePath, 'eatghost.ogg'))
click     = pygame.mixer.Sound(os.path.join(filePath, 'click.ogg'))
begin     = pygame.mixer.Sound(os.path.join(filePath, 'begin.ogg'))
music     = pygame.mixer.music.load(os.path.join(filePath, 'intermission.ogg'))

# --------- Set frequency --------- 
pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init(frequency=44100)

# --------- Game initialization & methods --------- 
class Game:
  def __init__(self, pacman, blinky, pinky, inky, clyde):
    self.DEBUG           = False
    self.run             = True
    self.pellets         = 0
    self.eaten           = 0
    self.pelletsCount    = PELLETS
    self.pacman          = pacman
    self.blinky          = blinky
    self.pinky           = pinky
    self.inky            = inky
    self.clyde           = clyde
    self.maze            = maze
    self.ghostResetTimer = 0
    self.chaseTime       = 0
    self.scatterTime     = 0
    self.score           = 0
    self.level           = 1
    self.savedScore      = 0
    self.savedLevel      = 1
    self.mode            = NORMAL
    self.lives           = 3
    self.text            = "GO"
    self.textColor       = GREEN
    self.fontSize        = 40
    self.locked          = False
    self.reset           = False
    self.pause           = True
    self.click           = False
    self.file = open("storage/score.pkl","rb")

  # Draw character sprite
  def generateSprite(self, sprites, face, x, y): return win.blit(sprites[face], (x,y))

  # Update map index
  def setIndex(self, new, x, y):
    previous = self.maze
    previous[y][x] = int(new)
    self.maze = previous

  # Blinking effect 
  def animateText(self, rate: int):
    for r in range(rate):
      pygame.time.delay(400)
      self.textColor = WHITE
      pygame.time.delay(400)
      self.textColor = YELLOW

  # Update level when pacman eats all the remaining pellets
  def updateLevel(self):
    self.level += 1
    self.pacman.resetPacman()
    self.blinky.resetGhost()
    self.pinky.resetGhost()
    self.inky.resetGhost()
    self.clyde.resetGhost()
    self.reset = True
    self.pelletsCount = PELLETS
    self.pellets = 0
    self.eaten = 0
    self.mode = 0
    self.text = f"Level {game.level}"
    self.fontSize = 40
    self.textColor = YELLOW

    for i in range(0, len(self.maze)):
      for j in range(0, len(self.maze[i])):
        if self.maze[i][j] == POWER_EAT:
          pygame.draw.circle(win, (237, 234, 206), ((j * CHAR_WIDTH) + 10, (i * CHAR_WIDTH) + 10), 1)
          self.setIndex(POWER, j, i)
        if self.maze[i][j] == NORMAL_PELLET_EAT:
          pygame.draw.circle(win, (237, 234, 206), ((j * CHAR_WIDTH) + 10, (i * CHAR_WIDTH) + 10), 1)
          self.setIndex(NORMAL_PELLET, j, i)

    threading.Thread(target=self.animateText(3)).start()
    if not self.DEBUG: pygame.mixer.music.unpause()

    self.locked = False

  # Welcome / Start / Pause screen
  def startScreen(self, text, color):
    win.blit(pygame.image.load("assets/start_background.png"), (0,0))
    win.blit(pygame.image.load("assets/logo.png"), (X//2 - 124, Y//2 - 150))
    button_1 = pygame.draw.rect(win, (54, 158, 211), (X//2 - 100, Y//2 + 30, 200, 50), 1)
    if button_1.collidepoint((mx, my)):
      win.blit(pygame.image.load("assets/start_clicked.png"), (X//2 - 100, Y//2 + 30))
      if self.click:
        pygame.mixer.Sound.play(click)
        pygame.time.delay(200)
        pygame.mixer.Sound.play(begin)
        game.pause = False
        if not self.DEBUG: pygame.mixer.music.unpause()
    else:
      win.blit(pygame.image.load("assets/start.png"), (X//2 - 100, Y//2 + 30))

  # Game over screen
  def gameOverEndScreen(self, text, color):
    pygame.mixer.music.pause()
    s = pygame.Surface((X,Y), pygame.SRCALPHA)
    s.fill((0,0,0,200))
    win.blit(s, (0,0))

    txt = Font(digit_font, 80).render(str(text), True, color)
    scoreText = txt.get_rect()
    scoreText.center = (X//2, (Y//2) - 70)
    win.blit(txt, scoreText)

    txt = Font(digit_font, 20).render("<Press space to restart>", True, (255,255,255))
    scoreText = txt.get_rect()
    scoreText.center = (X//2, (Y//2) - 20)
    win.blit(txt, scoreText)

    txt = Font(digit_font, 18).render("Your high scores are saved automatically", True, (255,255,255))
    scoreText = txt.get_rect()
    scoreText.center = (X//2, (Y//2) + 30)
    win.blit(txt, scoreText)

  # When the user presses a key, the character moves
  def walkCharacters(self):
    self.fontSize = 18
    self.textColor = GREEN
    self.text = "Press space to pause"
    self.pacman.vel = self.blinky.vel = self.pinky.vel = self.inky.vel = self.clyde.vel = 1

  # Generate pellets
  def generatePellets(self):
    for i in range(0, len(game.maze)):
      for j in range(0, len(game.maze[i])):
        if game.DEBUG: pygame.draw.rect(win, (35, 35, 35), ((j * CHAR_WIDTH), (i * CHAR_WIDTH), 20, 20), 1)

        if game.maze[i][j] == NORMAL_PELLET:
          pygame.draw.circle(win, (237, 234, 206), ((j * CHAR_WIDTH) + 10, (i * CHAR_WIDTH) + 10), 3)
        if game.maze[i][j] == POWER:
          pygame.draw.circle(win, (237, 234, 206), ((j * CHAR_WIDTH) + 10, (i * CHAR_WIDTH) + 10), 6)

  # Place Pacman on the map and watch for movement.
  def drawPlayer(self):
    self.pacman.control()

    if (self.pacman.x <= 0 and self.pacman.y == 240): self.pacman.x, self.pacman.y = 500+CHAR_WIDTH, 240
    elif (self.pacman.x >= 520 and self.pacman.y == 240): self.pacman.x, self.pacman.y = 0, 240

  # Place ghost on the map and watch for movement.
  def drawGhost(self, ghost):
    if ghost.display:
      ghost.control()

      if (ghost.x == 0 and ghost.y == 240): ghost.x, ghost.y = 520, 240
      elif (ghost.x == 520 and ghost.y == 240): ghost.x, ghost.y = 0, 240

      if ghost.stage == SCATTER:
        ghost.scatter()
      elif ghost.stage == CHASE:
        if ghost.name == "blinky": blinky_pattern()
        elif ghost.name == "pinky": pinky_pattern()
        elif ghost.name == "inky": inky_pattern()
        elif ghost.name == "clyde": clyde_pattern()

  # Display the game status text in the center of the screen.
  def displayStatus(self):
    txt = Font(digit_font, int(game.fontSize)).render(str(game.text), True, game.textColor)
    scoreText = txt.get_rect()
    scoreText.center = (X//2, (Y//2) - 60)
    win.blit(txt, scoreText)

  # Display the current game score, saved score, and number of player lives remaining.
  def displayNumbers(self):
    gameScoreTxt = Font(digit_font, 22).render(str(game.score), True, (60, 60, 60))
    gameSavedScoreTxt = Font(digit_font, 22).render(str(game.savedScore), True, (60, 60, 60))
    gameLevelTxt = Font(digit_font, 22).render(str(game.level), True, (60, 60, 60))

    gameScoreRect = gameScoreTxt.get_rect()
    gameSavedScoreRect = gameSavedScoreTxt.get_rect()
    gameLevelRect = gameLevelTxt.get_rect()

    gameScoreRect.left, gameScoreRect.top = 33, 544 
    gameSavedScoreRect.left, gameSavedScoreRect.top = 198, 544
    gameLevelRect.left, gameLevelRect.top = 33, 597

    win.blit(gameScoreTxt, gameScoreRect)
    win.blit(gameSavedScoreTxt, gameSavedScoreRect)
    win.blit(gameLevelTxt, gameLevelRect)

    for i in range(1, self.lives + 1): win.blit(pygame.image.load("assets/pac.png"), (X-193 + (i * 18), 544 + 6))

  # Start the game. Put the ghost, Pac-Man, and pellets on the map.
  def initialize(self):
    win.fill((0,0,0))
    win.blit(bg, (0, 0))
    self.generatePellets()
    self.drawPlayer()
    self.displayNumbers()
    self.drawGhost(blinky)
    self.drawGhost(pinky)
    self.drawGhost(inky)
    self.drawGhost(clyde)

  # Once the game is initiated, the game begins and the ghosts are released.
  def startGame(self):
    # clock.tick(83)
    clock.tick(100)
    dt = clock.tick()

    if not game.locked:
      self.blinky.toggleRelease() 
      if self.eaten >= int((0.20 if self.level > 0 and self.level < 3 else 0.10) * self.pelletsCount): self.inky.toggleRelease()
      if self.eaten >= int((0.40 if self.level > 0 and self.level < 3 else 0.20) * self.pelletsCount): self.clyde.toggleRelease()
      self.pinky.toggleRelease()

# --------- Pacman class --------- 
class Player:
  walkCount = 0

  def __init__(self, name, x, y):
    self.name         = name
    self.x            = x
    self.y            = y
    self.vel          = 0
    self.face         = 0
    self.die          = False
    self.nextFace     = 0
    self.contaminated = False

  # Reset player's position and state
  def resetPacman(self):
    self.x = characters[self.name]["coordinates"][0]
    self.y = characters[self.name]["coordinates"][1]
    self.die = False
    self.nextFace = 0
    self.face = 0
    self.vel = 0

  # Observes the environment around Pacman to determine whether the next step is a wall or a food.
  def getSurrounds(self):
    try:
      return [
        game.maze[((self.y + 10)//20)][((self.x + 10)//20)-1],
        game.maze[((self.y + 10)//20)][((self.x + 10)//20)+1],
        game.maze[((self.y + 10)//20)-1][((self.x + 10)//20)],
        game.maze[((self.y + 10)//20)+1][((self.x + 10)//20)]
      ]
    except IndexError: return

  # Move character 
  def move(self, arr, direction):
    if self.name != "pacman" and game.mode == FRIGHTENED and self.contaminated:
      if game.ghostResetTimer > 400: 
        if self.walkCount + 1 >= 18: self.walkCount = 0
        game.generateSprite(ghost_dead_sprites, self.walkCount//9, self.x, self.y)
        self.walkCount += 1
      else:
        game.generateSprite(ghost_dead_sprites, 0, self.x, self.y)
    else:
      if self.walkCount + 1 >= 18: self.walkCount = 0
      game.generateSprite(arr, self.walkCount//9, self.x, self.y)
      self.walkCount += 1

    if (direction == LEFT): self.x -= self.vel
    elif (direction == RIGHT): self.x += self.vel
    elif (direction == UP): self.y -= self.vel
    elif (direction == DOWN): self.y += self.vel

  # Wall and food detection
  def control(self):
    controllerX, controllerY = int((self.x - (self.x % 10)) // 20), int((self.y - (self.y % 10)) // 20)

    try:
      if self.face == 0 and self.name == 'pacman' and pacman.die:
        if self.walkCount <= 99:
          win.blit(death_sprites[self.walkCount//9], (self.x,self.y))
          self.walkCount += 1
      else:
        if self.face == STILL: game.generateSprite(characters[self.name]["sprites"], self.face, self.x, self.y)

      condition = (
        NORMAL_PELLET,
        NORMAL_PELLET_EAT,
        POWER,
        POWER_EAT,
        BLANK
      ) if self.name == "pacman" else (
        NORMAL_PELLET,
        NORMAL_PELLET_EAT,
        POWER,
        POWER_EAT,
        BLANK,
        GHOST_BARRIER
      )

      if self.face in (LEFT, RIGHT):
        if self.x == (self.x - (self.x % 10)) and self.x % 20 == 0:
          if game.maze[controllerY][controllerX - 1 if self.face == LEFT else controllerX + 1] in condition and not pacman.die:
            self.move(characters[self.name]["walkLeft"] if self.face == LEFT else characters[self.name]["walkRight"], self.face)
          else:
            game.generateSprite(characters[self.name]["sprites"], self.face, self.x, self.y)
        else:
          self.move(characters[self.name]["walkLeft"] if self.face == LEFT else characters[self.name]["walkRight"], self.face)

      if self.face in (UP, DOWN):
        if self.y == (self.y - (self.y % 10)) and self.y % 20 == 0:
          if game.maze[controllerY - 1 if self.face == UP else controllerY + 1][controllerX] in condition and not pacman.die:
            self.move(characters[self.name]["walkUp"] if self.face == UP else characters[self.name]["walkDown"], self.face)
          else:
            game.generateSprite(characters[self.name]["sprites"], self.face, self.x, self.y)
        else:
          self.move(characters[self.name]["walkUp"] if self.face == UP else characters[self.name]["walkDown"], self.face)
    except IndexError: return

# --------- Ghost class --------- 
class Enemy(Player):
  def __init__(self, name, x, y, scatterLocation):
    super().__init__(name, x, y)
    self.scatterLocation = scatterLocation
    self.restricted      = -1
    self.stage           = SCATTER
    self.released        = False
    self.display         = True

  # Remove the ghosts from the house
  def toggleRelease(self): self.released = not self.released

  # Reset the positions, faces, and velocity of the ghost.
  def resetGhost(self):
    self.display = True
    self.released = False
    self.face = STILL
    self.vel = 0
    self.x = characters[self.name]["coordinates"][0]
    self.y = characters[self.name]["coordinates"][1]

  # Reset character parameters
  def resetCharacters(self):
    pacman.die = True
    blinky.display = pinky.display = inky.display = clyde.display = False
    pygame.time.delay(1600)
    if not game.DEBUG: pygame.mixer.Sound.play(death)
    pacman.face = STILL
    pacman.nextFace = STILL
    pygame.time.delay(1400)
    game.lives -= 1
    
    pacman.resetPacman()
    blinky.resetGhost()
    inky.resetGhost()
    pinky.resetGhost()
    clyde.resetGhost()

    if game.lives > 0:
      for i in range(3, 0, -1):
        if not game.DEBUG: pygame.mixer.Sound.play(count)
        game.text = str(i)
        game.textColor = GREEN
        game.fontSize = 40
        pygame.time.delay(1000)
      if not game.DEBUG: pygame.mixer.Sound.play(go)
      game.fontSize = 40
      game.text = "GO"
      game.textColor = GREEN
      pygame.time.delay(600)
    else:
      pygame.time.delay(1000)
      if not game.DEBUG: pygame.mixer.Sound.play(gameover)

    if not game.DEBUG: pygame.mixer.music.unpause()
    game.locked = False
    pacman.face = pacman.nextFace

    if not game.reset:
      if game.lives > 0:
        pacman.face = LEFT
        game.walkCharacters()
        game.reset = False
      else:
        pygame.mixer.music.pause()

  # Determine whether a ghost eats Pacman or Pacman eats a ghost.
  def eat(self):
    distance = sqrt(((pacman.x-10)-(self.x-10))**2 + ((pacman.y-10)-(self.y-10))**2)
    if distance < 10:
      if game.mode == NORMAL or (not self.contaminated and game.mode == FRIGHTENED):

        game.pelletsCount = 191 - game.pellets
        game.eaten = 0

        game.locked = True
        try:
          threading.Thread(target=self.resetCharacters).start()
        except (KeyboardInterrupt, SystemExit):
          sys.exit()
      else:
        game.score += 100
        self.contaminated = False
        if not game.DEBUG: pygame.mixer.Sound.play(eatGhost)
        pygame.time.delay(600)
        self.resetGhost()

  # Disperse ghosts to their designated scatter locations
  def scatter(self): self.pointTo(self.scatterLocation)

  # Chase mode
  def chase(self, coords=(20, 20)): self.pointTo(coords)

   # Point Ghost in a specific direction
  def pointTo(self, coordinates=(20, 20)):
    surrounds = self.getSurrounds()
    d0 = d1 = d2 = d3 = X*Y

    allowedDirections = [i for i in range(0, 4) if i != self.restricted]

    try:
      for direction in allowedDirections:
        if surrounds[direction] in (NORMAL_PELLET, NORMAL_PELLET_EAT, POWER, POWER_EAT, BLANK, GHOST_BARRIER):
          x2, y2 = coordinates[0], coordinates[1]
          if direction == 0:
            x1, y1 = self.x - 20, self.y
            d0 = sqrt((x2 - x1)**2 + (y2 - y1)**2)
          elif direction == 1:
            x1, y1 = self.x + 20, self.y
            d1 = sqrt((x2 - x1)**2 + (y2 - y1)**2)
          elif direction == 2:
            x1, y1 = self.x, self.y - 20
            d2 = sqrt((x2 - x1)**2 + (y2 - y1)**2)
          elif direction == 3:
            x1, y1 = self.x, self.y + 20
            d3 = sqrt((x2 - x1)**2 + (y2 - y1)**2)

      if game.DEBUG:
        pygame.draw.line(win, characters[self.name]["theme"], (self.x + 10, self.y + 10), (coordinates[0]+10, coordinates[1]+10), width=2)
        pygame.draw.circle(win, characters[self.name]["theme"], (coordinates[0]+10, coordinates[1]+10), 5)

      if (self.x % 20 == 0 and self.y % 20 == 0):
        distances = [d0, d1, d2, d3]
        lowest = min(distances)
        face = distances.index(lowest)
        if face == 0: self.restricted = 1
        elif face == 1: self.restricted = 0
        elif face == 2: self.restricted = 3
        elif face == 3: self.restricted = 2
        if self.released: self.face = face + 1
    except TypeError: return

pacman = Player(
    "pacman",
    characters["pacman"]["coordinates"][0],
    characters["pacman"]["coordinates"][1])

blinky = Enemy(
    "blinky",
    characters["blinky"]["coordinates"][0],
    characters["blinky"]["coordinates"][1],
    characters["blinky"]["scatterLocation"])

pinky = Enemy(
    "pinky",
    characters["pinky"]["coordinates"][0],
    characters["pinky"]["coordinates"][1],
    characters["pinky"]["scatterLocation"])

inky = Enemy(
    "inky",
    characters["inky"]["coordinates"][0],
    characters["inky"]["coordinates"][1],
    characters["inky"]["scatterLocation"])

clyde = Enemy(
    "clyde",
    characters["clyde"]["coordinates"][0],
    characters["clyde"]["coordinates"][1],
    characters["clyde"]["scatterLocation"])

ghosts = [ blinky, pinky, inky, clyde ]
game = Game(pacman, blinky, pinky, inky, clyde)

# Reverse the current direction of the ghost when pacman eats a power pellet
def reverse_pattern(character):
  if character.face   == LEFT: character.face  == RIGHT
  elif character.face == RIGHT: character.face == LEFT
  elif character.face == UP: character.face    == DOWN
  elif character.face == DOWN: character.face  == UP
  character.scatter()

# --------- Ghost patterns to trap pacman --------- 
def blinky_pattern():
  if game.mode == NORMAL: blinky.chase((pacman.x, pacman.y))
  else: reverse_pattern(blinky)

def pinky_pattern():
  if game.mode == NORMAL:
    if pacman.face   == LEFT: pinky.chase((pacman.x - 40, pacman.y))
    elif pacman.face == RIGHT: pinky.chase((pacman.x + 40, pacman.y))
    elif pacman.face == UP: pinky.chase((pacman.x - 40, pacman.y - 40))
    elif pacman.face == DOWN: pinky.chase((pacman.x, pacman.y + 40))
  else:
    reverse_pattern(pinky)

def inky_pattern():
  if game.mode == NORMAL:
    newPosX, newPosY = 0, 0
    if pacman.face   == LEFT: newPosX, newPosY  = pacman.x - (2 * 20), pacman.y
    elif pacman.face == RIGHT: newPosX, newPosY = pacman.x + (2 * 20), pacman.y
    elif pacman.face == UP: newPosX, newPosY    = pacman.x - (2 * 20), pacman.y - (2 * 20)
    elif pacman.face == DOWN: newPosX, newPosY  = pacman.x, pacman.y + (2 * 20)

    if (blinky.y < newPosY): inky.chase((pacman.x - ((abs(newPosX - blinky.x) / 20) * 20), pacman.y + ((abs(newPosY - blinky.y) / 20) * 20)))
    else: inky.chase((pacman.x - ((abs(newPosX - blinky.x) / 20) * 20), pacman.y - ((abs(newPosY - blinky.y) / 20) * 20)))
  else:
    reverse_pattern(inky)

def clyde_pattern():
  if game.mode == NORMAL:
    distance = sqrt((pacman.x - clyde.x)**2 + (pacman.y - clyde.y)**2)
    if (distance / 20) > 8: clyde.chase((pacman.x, pacman.y))
    else: clyde.scatter()
  else:
    reverse_pattern(clyde)

if not game.DEBUG: pygame.mixer.music.play(-1, 0.0)

# Load saved score and level
try:
  state = pickle.load(game.file)
  game.savedLevel = int(state["level"])
  game.savedScore = int(state["score"])
  game.file.close()
except EOFError:
  game.savedLevel = 1
  game.savedScore = 0

while game.run:
  mx, my = pygame.mouse.get_pos() 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      game.run = False
      sys.exit(0)
    if event.type == MOUSEBUTTONDOWN:
      if event.button == 1: game.click = True

    if event.type == pygame.KEYDOWN:
      # Reset all game settings and ghost positions when players loses all its three lives
      if (event.key == pygame.K_SPACE and game.lives == 0):
        pacman.resetPacman()
        blinky.resetGhost()
        pinky.resetGhost()
        inky.resetGhost()
        clyde.resetGhost()

        # Reset pellet states
        for i in range(0, len(game.maze)):
          for j in range(0, len(game.maze[i])):
            if game.maze[i][j] == POWER_EAT:
              pygame.draw.circle(win, (237, 234, 206), ((j * CHAR_WIDTH) + 10, (i * CHAR_WIDTH) + 10), 1)
              game.maze[i][j] = POWER
            if game.maze[i][j] == NORMAL_PELLET_EAT:
              pygame.draw.circle(win, (237, 234, 206), ((j * CHAR_WIDTH) + 10, (i * CHAR_WIDTH) + 10), 1)
              game.maze[i][j] = NORMAL_PELLET


        game.pellets      = 0
        game.pelletsCount = PELLETS
        game.eaten        = 0
        game.locked       = False
        game.reset        = True
        game.lives        = 3
        game.score        = 0
        game.level        = 1
        if not game.DEBUG: pygame.mixer.music.unpause()

  keys = pygame.key.get_pressed()

  if keys[K_SPACE] and game.lives != 0:
    pygame.mixer.Sound.play(click)
    pygame.time.delay(300)
    pygame.mixer.Sound.play(begin)
    game.pause = not game.pause
    game.click = not game.click

  if game.pause:
    game.startScreen("Hello World", (255,0,0))
  else:
    # When pacman eats all pellets, change the level
    if game.pellets >= PELLETS:
      game.locked = True
      threading.Thread(target=game.updateLevel).start()
    # pause background music when pacman dies
    if pacman.die: pygame.mixer.music.pause()

    # After some time, the ghost state is reset from frightened mode to normal mode.
    if game.mode == FRIGHTENED:
      game.ghostResetTimer += 1
    if game.ghostResetTimer > 600:
      game.mode = NORMAL
      game.ghostResetTimer = 0

    if not game.locked and pacman.vel == 1:
      for ghost in ghosts: ghost.eat()

      game.chaseTime += 1
      game.scatterTime += 1

      # switch to chase and scatter after some time
      if game.chaseTime > 250:
        for ghost in ghosts: ghost.stage = CHASE
      if game.chaseTime > 650:
        for ghost in ghosts: ghost.stage = SCATTER
        game.chaseTime = 0
        game.scatterTime = 0

    if not game.locked:
      if not pacman.die and game.lives > 0:
        # Save key direction to predict next face
        if keys[pygame.K_LEFT]:
          pacman.nextFace = LEFT
          game.walkCharacters()
        if keys[pygame.K_RIGHT]:
          pacman.nextFace = RIGHT
          game.walkCharacters()
        if keys[pygame.K_UP]:
          pacman.nextFace = UP
          game.walkCharacters()
        if keys[pygame.K_DOWN]:
          pacman.nextFace = DOWN
          game.walkCharacters()

        conditions = (NORMAL_PELLET, NORMAL_PELLET_EAT, POWER, POWER_EAT, BLANK)

        try:
          # move only when coordinate and state is valid
          if (pacman.x % 20 == 0 and pacman.y % 20 == 0):
            if keys[pygame.K_LEFT] and pacman.getSurrounds()[0] in conditions:  pacman.face = LEFT
            if keys[pygame.K_RIGHT] and pacman.getSurrounds()[1] in conditions: pacman.face = RIGHT
            if keys[pygame.K_UP] and pacman.getSurrounds()[2] in conditions:    pacman.face = UP
            if keys[pygame.K_DOWN] and pacman.getSurrounds()[3] in conditions:  pacman.face = DOWN

            if pacman.getSurrounds()[pacman.nextFace - 1] in conditions: pacman.face = pacman.nextFace
        except TypeError: None

      # state in the maze array 
      index = game.maze[pacman.y//20][pacman.x//20]

      # change state when pacman steps on pellets 
      if index == 0:
        game.score += 10
        game.pellets += 1
        game.eaten += 1
        if not game.DEBUG: pygame.mixer.Sound.play(chomp)
        game.setIndex(6, pacman.x//20, pacman.y//20)

      if index == 5:
        game.score += 50
        game.pellets += 1
        game.eaten += 1
        game.mode = FRIGHTENED
        blinky.contaminated = pinky.contaminated = inky.contaminated = clyde.contaminated = True
        if not game.DEBUG: pygame.mixer.Sound.play(bonus)
        game.setIndex(4, pacman.x//20, pacman.y//20)

    # If Pacman still has lives, keep playing the game. If this isn't the case, lock the keys and reset the characters.
    try:
      if (game.lives > 0):
        game.initialize()
        game.startGame()
        game.displayStatus()
      else:
        game.locked = True
        game.initialize()
        game.startGame()
        game.gameOverEndScreen("GAME OVER", (255,0,0))
        pygame.time.delay(1200)
    except IndexError:
      print("Error")

    # update saved high score
    if game.score > game.savedScore:
      game.savedScore = game.score
      data = { "score": game.score, "level": game.level }
      pickle.dump(data, open("storage/score.pkl","wb"))
      game.file.close()

  pygame.display.update() 

pygame.quit()

