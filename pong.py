import time, os, ast, pygame, threading, platform, random, logging
from _thread import *
from customEnums import *

#Basic Logging
logging.basicConfig(level=logging.INFO)

fileLogger = logging.getLogger("pongFileLogger")
fileHandler = logging.FileHandler("pongLog.log")
fileFormatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler.setFormatter(fileFormatter)
fileLogger.addHandler(fileHandler)
fileLogger.setLevel(logging.INFO)

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
hit1 = 0
hit2 = 0
total1 = 0
total2 = 0
currentGameMode = GameModes.zeroPlayers
predictedNumLock = threading.Lock()
predictedNum = 0

#BASIC CONSTANTS
WIDTH = 1200
HEIGHT = 600
FRAMERATECAP = 60
TICKSPERSECOND = 100

#BOT CHOICE LISTS
easyBotList = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
mediumBotList = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
hardBotList = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
impossibleBotList = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

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

	def getCurrentSpeeds(self):
		return (self.currentXSpeed, self.currentYSpeed)

	def paddleHit(self):
		global total1, total2
		self.currentXSpeed *= -1
		if self.currentXSpeed > 0:
			total1 += 1
		elif self.currentXSpeed < 0:
			total2 += 1

	def update(self):
		global score1, score2, hit1, hit2
		self.rect.x += self.currentXSpeed
		self.rect.y += self.currentYSpeed

		if pygame.sprite.spritecollide(self, Paddles, False):
			if not (self.rect.left < 58 or self.rect.right > (WIDTH - 70)):
				self.paddleHit()

		if self.rect.x >= WIDTH - 20:
			score1 += 1
			hit2 += 1
			self.reset()
		elif self.rect.x <= 0:
			score2 += 1
			hit1 += 1
			self.reset()
		if self.rect.y <= 0:
			self.currentYSpeed *= -1
		elif self.rect.bottom >= HEIGHT:
			self.currentYSpeed *= -1

class Bot():
	def __init__(self, paddleNum):
		self.paddle = paddleNum
		self.predictedPosition = WIDTH/2
		self.difficulty = BotDiffs.medium

	def setDifficulty(self, diff):
		self.difficulty = diff

	def getRandomOffset(self):
		offsetChoice = 1
		offset = 100
		
		if self.difficulty == BotDiffs.easy:
			offsetChoice = random.choice(easyBotList)
		elif self.difficulty == BotDiffs.medium:
			offsetChoice = random.choice(mediumBotList)
		elif self.difficulty == BotDiffs.hard:
			offsetChoice = random.choice(hardBotList)
		elif self.difficulty == BotDiffs.impossible:
			offsetChoice = random.choice(impossibleBotList)
		
		if offsetChoice == 0:
			if random.choice([True, False]):
				return offset
			else:
				offset *= -1
		elif offsetChoice == 1:
			offset = 0

		return offset
	
	def predictBall(self):
		#Meant to predict the ball's position when it's moving towards the bot's side
		global predictedNum
		ballXSpeed, ballYSpeed = ball.getCurrentSpeeds()
		ballX, ballY = ball.rect.center
		if self.paddle == 2:
			slope, x, a, b = ((ballYSpeed / ballXSpeed), paddle2.rect.left, ballX, ballY)
			bYCS = ballYSpeed
			while True:
				tempVar = -1 * getYFromPointSlope(slope, x, a, b)
				if tempVar < 0 or tempVar > HEIGHT:
					if bYCS < 0:
						var = getXFromPointSlope(slope, 0, a, b)
						a = var
						b = 0
					else:
						var = getXFromPointSlope(slope, -600, a, b)
						a = var
						b = 600
					slope *= -1
					bYCS *= -1
				elif tempVar >= 0 and tempVar <= HEIGHT:
					returnValue = tempVar
					break
		
		elif self.paddle == 1:
			slope, x, a, b = ((ballYSpeed / ballXSpeed), paddle1.rect.right, ballX, ballY)
			bYCS = ballYSpeed
			while True:
				tempVar = -1 * getYFromPointSlope(slope, x, a, b)
				if tempVar < 0 or tempVar > HEIGHT:
					if bYCS < 0:
						var = getXFromPointSlope(slope, 0, a, b)
						a = var
						b = 0
					else:
						var = getXFromPointSlope(slope, -600, a, b)
						a = var
						b = 600
					slope *= -1
					bYCS *= -1
				elif tempVar >= 0 and tempVar <= HEIGHT:
					returnValue = tempVar
					break

		return returnValue + self.getRandomOffset()

#save		returnValue = -1 * ((-1 * (ballYSpeed / ballXSpeed)) * (paddle1.rect.right - ballX) - ballY)

	def movePaddle(self, yPos):
		global up2, down2, up, down
		if self.paddle == 2:
			paddleX, paddleY = paddle2.rect.center
			if paddleY > yPos + 2:
				up2 = True
				down2 = False
			elif paddleY < yPos - 2:
				down2 = True
				up2 = False
			else:
				up2 = False
				down2 = False
		elif self.paddle == 1:
			paddleX, paddleY = paddle1.rect.center
			if paddleY > yPos + 3:
				up = True
				down = False
			elif paddleY < yPos - 3:
				down = True
				up = False
			else:
				up = False
				down = False

	def checkForPosUpdate(self):
		if ball.rect.left < 58 or ball.rect.right > (WIDTH - 70):
			return False
		if ball.rect.y <= 25 or ball.rect.y >= (HEIGHT - 25):
			if self.paddle == 2:
				bXCS, bYCS = ball.getCurrentSpeeds()
				if bXCS > 0:
					return True
			elif self.paddle == 1:
				bXCS, bYCS = ball.getCurrentSpeeds()
				if bXCS < 0:
					return True
		elif ball.rect.right >= (paddle2.rect.left - 5):
			bXCS, bYCS = ball.getCurrentSpeeds()
			if bXCS < 0:
				return True
		elif ball.rect.left <= (paddle1.rect.right + 5):
			bXCS, bYCS = ball.getCurrentSpeeds()
			if bXCS > 0:
				return True
		else:
			return False

	def update(self):
		if self.checkForPosUpdate():
			self.predictedPosition = self.predictBall()
		if self.paddle == 2:
			if abs(paddle2.rect.center[1] - self.predictedPosition) >= abs(ball.rect.right - paddle2.rect.left):
				self.movePaddle(self.predictedPosition)
			else:
				self.movePaddle(paddle2.rect.center[1])
		elif self.paddle == 1:
			if abs(paddle1.rect.center[1] - self.predictedPosition) >= abs(ball.rect.left - paddle1.rect.right) :
				self.movePaddle(self.predictedPosition)
			else:
				self.movePaddle(paddle1.rect.center[1])

ball = Ball()
paddle1 = Paddle(50, (HEIGHT/2) - 50)
paddle2 = Paddle(WIDTH - 75, (HEIGHT/2) - 50)
bot1 = Bot(2)
bot1.setDifficulty(BotDiffs.impossible)
bot2 = Bot(1)
bot2.setDifficulty(BotDiffs.hard)

#FUNCTIONS
def getYFromPointSlope(slope, x, a, b):
	return ((-1 * slope) * (x - a) - b)

def getXFromPointSlope(slope, y, a, b):
	return (((y + b) / (-1 * slope)) + a)

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
		
		#Cool prediction lines		
		"""bXCS, bYCS = ball.getCurrentSpeeds()
		if bYCS < 0:
			pygame.draw.line(gameDisplay, GREEN, ball.rect.center, (getXFromPointSlope((bYCS/bXCS), 0, ball.rect.x, ball.rect.y), 0))
		else:
			pygame.draw.line(gameDisplay, GREEN, ball.rect.center, (getXFromPointSlope((bYCS/bXCS), -1 * HEIGHT, ball.rect.x, ball.rect.y), HEIGHT))"""

		pygame.display.set_caption("Pong " + str(clock.get_fps()))
		clock.tick(FRAMERATECAP)
		pygame.display.update()

start_new_thread(render, ())

#Game loop
#fileLogger.info("Starting game loop")
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
				if currentGameMode == GameModes.twoPlayers:
					up2 = True
			elif event.key == pygame.K_DOWN:
				if currentGameMode == GameModes.twoPlayers:
					down2 = True
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				up = False
			elif event.key == pygame.K_s:
				down = False
			elif event.key == pygame.K_UP:
				if currentGameMode == GameModes.twoPlayers:
					up2 = False
			elif event.key == pygame.K_DOWN:
				if currentGameMode == GameModes.twoPlayers:
					down2 = False

	#Game logic
	if currentGameMode == GameModes.onePlayer:
		bot1.update()
	elif currentGameMode == GameModes.zeroPlayers:
		bot1.update()
		bot2.update()

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

	addMessage(str(score1), WHITE, 100, 20)
	addMessage(str(score2), WHITE, (WIDTH - 150), 20)

	addMessage("BW" + str(hit1), WHITE, 150, 40)
	addMessage("BW" + str(hit2), WHITE, (WIDTH - 200), 40)

	addMessage("PH" + str(total1), WHITE, 150, 60)
	addMessage("PH" + str(total2), WHITE, (WIDTH - 200), 60)

	addMessage("T" + str(total1+hit1), WHITE, 150, 80)
	addMessage("T" + str(total2+hit2), WHITE, (WIDTH - 200), 80)

	try:
		addMessage("P" + str((total1+hit1) / total1), WHITE, 150, 100)
		addMessage("P" + str((total2+hit2) / total2), WHITE, (WIDTH - 200), 100)
	except:
		herblferblgerbl = 1

	#Make sure the logic stays at a decent rate
	logicClock.tick(TICKSPERSECOND)