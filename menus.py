import pygame.sprite

pygame.font.init()
font = pygame.font.SysFont("Arial", 25)

def gui(x1, y1, x2, y2, button):
	mouseX, mouseY = pygame.mouse.get_pos()
	if mouseX >= x1 and mouseX <= x2 and mouseY >= y1 and mouseY <= y2:
		if button:
			return True
		else:
			return False
	else:
		return False

class MenuPanel:
	def __init__(self):
		self.buttons = []
		self.texts = []
		self.closeMenu = False

	def addButton(self, buttonObj):
		self.buttons.append(buttonObj)

	def addText(self, textObj):
		self.texts.append(textObj)

	def getButtons(self):
		return self.buttons

	def getTexts(self):
		return self.texts

	def checkCloseMenu(self):
		for button in self.buttons:
			if button.callCloseMenu:
				self.closeMenu = True
				break
		return self.closeMenu

	def checkForButtonPress(self):
		for button in self.buttons:
			mouseLeft, mouseMiddle, mouseRight = pygame.mouse.get_pressed()
			#print(f"x1: {button.rect.x}; y1: {button.rect.y}; x2: {button.rect.x + button.width}; y2: {button.rect.y + button.height}; mouseVal: {mouseLeft}")
			if gui(button.rect.x, button.rect.y, button.rect.x + button.width, button.rect.y + button.height, mouseLeft):
				button.onClick()

	def render(self, drawSurface):
		for button in self.buttons:
			button.draw(drawSurface)
		for text in self.texts:
			text.draw(drawSurface)

class Button(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, backgroundColor, text, textColor, eventHandler, args=[], preInverted = False):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((width, height))
		self.image.fill(backgroundColor)
		self.rect = self.image.get_rect(center=(x, y))

		self.eventHandler = eventHandler
		self.args = args
		self.backgroundColor = backgroundColor
		self.width, self.height = (width, height)
		self.text, self.textColor = (text, textColor)
		self.callCloseMenu = False
		if preInverted:
			self.inverted = True
		else:
			self.inverted = False

	def onClick(self):
		try:
			if self.eventHandler(self.args):
				self.callCloseMenu = True
		except TypeError:
			if self.eventHandler():
				self.callCloseMenu = True

	def updateText(self, updatedText):
		self.text = updatedText

	def invertColors(self):
		tempTextColor, tempBackColor = (self.textColor, self.backgroundColor)
		self.textColor = tempBackColor
		self.backgroundColor = tempTextColor
		self.image.fill(self.backgroundColor)
		if self.inverted:
			self.inverted = False
		elif not self.inverted:
			self.inverted = True

	def message_to_surface(self, msg, color, x, y, surface):
		screen_text = font.render(msg, True, color)
		surface.blit(screen_text, [x,y])
	
	def draw(self, drawSurface):
		self.message_to_surface(str(self.text), self.textColor, 5, 5, self.image)
		drawSurface.blit(self.image, [self.rect.x, self.rect.y])

class Text(pygame.sprite.Sprite):
	def __init__(self, x, y, text, textColor):
		pygame.sprite.Sprite.__init__(self)
		self.x, self.y = (x, y)
		self.text, self.textColor = (text, textColor)

	def message_to_surface(self, msg, color, x, y, surface):
		screen_text = font.render(msg, True, color)
		surface.blit(screen_text, [x,y])

	def draw(self, drawSurface):
		self.message_to_surface(self.text, self.textColor, self.x, self.y, drawSurface)