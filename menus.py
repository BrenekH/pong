import pygame

class MenuPanel:
	def __init__(self):
		self.buttons = []
		self.texts = []

	def addButton(self, buttonObj):
		self.buttons.append(buttonObj)

	def addText(self, textObj):
		self.texts.append(textObj)

	def render(self):
		for button in self.buttons:
			button.draw()
		for text in self.texts:
			text.draw()

class Button(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.__init__(self)
	
	def draw(self):
		return

class Text(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.__init__(self)

	def draw(self):
		return