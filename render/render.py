import pygame

class Render:
	def  __init__(self):
		pygame.init()
		self.surface = pygame.display.set_mode((1920, 1080))
		pygame.RESIZABLE
		self.run = True

	def on_event(self, event: pygame.event.Event):
		if event.type == pygame.QUIT:
			self.run = False

	def on_exec(self):
		while self.run:
			for event in pygame.event.get():
				self.on_event(event)
			pygame.display.update()
