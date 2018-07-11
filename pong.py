import time, os, ast, pygame, threading, platform, random
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
up2 = False
down2 = False
up = False
down = False
messageList = []
mLLock = threading.Lock()
score1 = 0
score2 = 0

#BASIC CONSTANTS
WIDTH = 1200
HEIGHT = 600
FRAMERATECAP = 60
TICKSPERSECOND = 100

#INIT PYGAME THINGS
pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
logicClock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

#SPRITE GROUPS
mainSpritesLayered = pygame.sprite.LayeredUpdates()

Paddles = pygame.sprite.Group()
Balls = pygame.sprite.Group()

#CLASSES
class Button(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class Paddle(pygame.sprite.Sprite):
	def __init__(self, rX, rY):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((25, 100))
		self.rect = self.image.get_rect(center=(rX, rY))
		self.image.fill(WHITE)

		self.resetX = rX
		self.resetY = rY
		self.speed = 5

		mainSpritesLayered.add(self, layer = 11)
		Paddles.add(self)

	def reset(self):
		self.rect.center = (self.resetX, self.resetY)
	
	def update(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		elif self.rect.bottom >= HEIGHT:
			self.rect.bottom = HEIGHT

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((20, 20))
		self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/2))
		self.image.fill(WHITE)

		self.xSpeed = 5
		self.ySpeed = 5

		self.reset()

		mainSpritesLayered.add(self, layer=10)
		Balls.add(self)

	def reset(self):
		self.rect.center = (WIDTH/2, HEIGHT/2)
		randList = []
		for x in range(2):
			randList.append(random.randrange(0,2))

		if randList[0] == 1:
			self.currentXSpeed = self.xSpeed * -1
		else:
			self.currentXSpeed = self.xSpeed

		if randList[1] == 1:
			self.currentYSpeed = self.ySpeed * -1
		else:
			self.currentYSpeed = self.ySpeed

		for paddle in Paddles:
			paddle.reset()

	def paddleHit(self):
		self.currentXSpeed *= -1

	def update(self):
		global score1, score2
		self.rect.x += self.currentXSpeed
		self.rect.y += self.currentYSpeed

		if pygame.sprite.spritecollide(self, Paddles, False):
			if not (self.rect.left < 58 or self.rect.right > (WIDTH - 70)):
				self.paddleHit()

		if self.rect.x >= WIDTH - 20:
			score1 += 1
			self.reset()
		elif self.rect.x <= 0:
			score2 += 1
			self.reset()
		if self.rect.y <= 0:
			self.currentYSpeed *= -1
		elif self.rect.bottom >= HEIGHT:
			self.currentYSpeed *= -1

ball = Ball()
paddle1 = Paddle(50, (HEIGHT/2) - 50)
paddle2 = Paddle(WIDTH - 75, (HEIGHT/2) - 50)

#FUNCTIONS
def message_to_surface(msg, color, x, y, surface):
	screen_text = font.render(msg, True, color)
	surface.blit(screen_text, [x,y])

def message_to_screen(msg, color, x, y):
	message_to_surface(msg, color, x, y, gameDisplay)

def addMessage(msg, color, x, y):
	global messageList
	with mLLock:
		messageList.append({"message": msg, "color": color, "x": x, "y": y})

def render():
	global messageList, logicClock
	while running:
		gameDisplay.fill(BLACK)

		with mLLock:
			copyMessageList = messageList
			messageList = []

		for Message in copyMessageList:
			message_to_screen(Message["message"], Message["color"], Message["x"], Message["y"])

		mainSpritesLayered.draw(gameDisplay)

		message_to_screen(str(logicClock.get_fps()), WHITE, 0, 570)
		pygame.display.set_caption("Pong " + str(clock.get_fps()))
		clock.tick(FRAMERATECAP)
		pygame.display.update()

start_new_thread(render, ())

#Game loop
while running:
	#Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				up = True
			elif event.key == pygame.K_s:
				down = True
			elif event.key == pygame.K_UP:
				up2 = True
			elif event.key == pygame.K_DOWN:
				down2 = True
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				up = False
			elif event.key == pygame.K_s:
				down = False
			elif event.key == pygame.K_UP:
				up2 = False
			elif event.key == pygame.K_DOWN:
				down2 = False

	#Game logic
	if up:
		paddle1.rect.y -= paddle1.speed
	if down:
		paddle1.rect.y += paddle1.speed
	if up2:
		paddle2.rect.y -= paddle2.speed
	if down2:
		paddle2.rect.y += paddle2.speed

	ball.update()
	Paddles.update()

	addMessage(str(score1), WHITE, 50, 20)
	addMessage(str(score2), WHITE, (WIDTH - 100), 20)

	#Make sure the logic stays at a decent rate
	logicClock.tick(TICKSPERSECOND)