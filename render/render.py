import pygame
from typing import Tuple

class Button:
	def __init__(self, text: str, height: int, width: int, func: callable):
		self.text = text
		self.width = width
		self.height = height
		self.func = func
		self.focus = False

	def draw(self, surface: pygame.Surface, font: pygame.font.Font):
		w_x, w_y = pygame.display.get_window_size()
		lenght, height = font.size(self.text)
		if self.focus:
			surface.blit(font.render("> ", False, "white"), (w_x / (100 / 30), w_y / (100 / self.height) - height / 2))
		surface.blit(font.render(self.text, False, "white"), (w_x / (100 / self.width) - lenght / 2, w_y / (100 / self.height) - height / 2))


class Render:
	def  __init__(self):
		pygame.init()
		self.surface = pygame.display.set_mode((1920, 1080))
		pygame.RESIZABLE
		self.run = True
		self.font = pygame.font.Font("font/ARCADE_N.TTF", 32)
		self.button = []
		self.menu = True
		self.focus = 0

	def on_event(self, event: pygame.event.Event):
		if event.type == pygame.QUIT:
			self.run = False
		if self.menu:
			self.button[self.focus].focus = True
			if event.type == pygame.KEYDOWN:
				match event.key:
					case pygame.K_DOWN:
						self.button[self.focus].focus = False
						self.focus = (self.focus + 1) % len(self.button)
						self.button[self.focus].focus = True
					case pygame.K_UP:
						self.button[self.focus].focus = False
						if self.focus == 0:
							self.focus = len(self.button) - 1
						else:
							self.focus = self.focus - 1
							self.button[self.focus].focus = True
					case pygame.K_SPACE:
						self.button[self.focus].func()

	def on_render(self):
		for button in self.button:
			button.draw(self.surface, self.font)

	def on_exec(self):
		self.button.append(Button("1 PLAYER", 55, 50, print))
		self.button.append(Button("2 PLAYERS", 65, 50, print))
		self.button.append(Button("EXIT", 75, 50, self.quit))
		while self.run:
			for event in pygame.event.get():
				self.on_event(event)
			self.surface.fill("black")
			self.on_render()
			pygame.display.update()

	def quit(self):
		self.run = False
