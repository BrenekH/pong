import time, os, ast, pygame #,oss
from _thread import *

#VARS

#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#GAME LOOP
running = True
currentTime = 0.0
lastFrameTime = 0.0
left = False
right = False
up = False
down = False

#BASIC CONSTANTS
WIDTH = 1200
HEIGHT = 600
FRAMERATECAP = 60
TICKSPERSECOND = 100

#INIT PYGAME THINGS
pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#SPRITE GROUPS
mainSpritesLayered = pygame.sprite.LayeredUpdates()

Platforms = pygame.sprite.Group()
Balls = pygame.sprite.Group()

#CLASSES
class Button(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class Platform(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 100))
		self.rect = self.image.get_rect()
		self.image.fill(WHITE)

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((20, 20))
		self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/2))
		self.image.fill(WHITE)

		self.xSpeed = 150
		self.ySpeed = 150
		self.translationVec = (self.xSpeed, self.ySpeed)
		
		mainSpritesLayered.add(self, layer=10)
		Balls.add(self)

	def update(self, delta):
		if self.rect.x >= WIDTH - 20:
			self.rect.x = WIDTH - 20
		elif self.rect.x <= 0:
			self.rect.x = 0
		if self.rect.y <= 0:
			self.rect.y = 0
		elif self.rect.bottom >= HEIGHT:
			self.rect.bottom = HEIGHT

ball = Ball()

#FUNCTIONS
def message_to_screen(msg, color, x, y):
	screen_text = font.render(msg, True, color)
	gameDisplay.blit(screen_text, [x,y])

def message_to_surface(msg, color, x, y, surface):
	screen_text = font.render(msg, True, color)
	surface.blit(screen_text, [x,y])

def render():
	while running:
		gameDisplay.fill(BLACK)

		mainSpritesLayered.draw(gameDisplay)

		clock.tick(FRAMERATECAP)
		pygame.display.update()

start_new_thread(render, ())

#Game loop
while running:
	currentTime = time.time()
	delta = currentTime - lastFrameTime
	#print(delta)
	sleepTime = 1./TICKSPERSECOND - (currentTime - lastFrameTime)
	if sleepTime > 0:
		time.sleep(sleepTime)
	lastFrameTime = currentTime
	#Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				up = True
			elif event.key == pygame.K_s:
				down = True
			elif event.key == pygame.K_a:
				left = True
			elif event.key == pygame.K_d:
				right = True
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				up = False
			elif event.key == pygame.K_s:
				down = False
			elif event.key == pygame.K_a:
				left = False
			elif event.key == pygame.K_d:
				right = False

	if up:
		ball.rect.y -= (ball.ySpeed * delta)
	if down:
		ball.rect.y += (ball.ySpeed * delta)
	if left:
		ball.rect.x -= (ball.xSpeed * delta)
	if right:
		ball.rect.x += (ball.xSpeed * delta)

	#Game logic
	ball.update(delta)