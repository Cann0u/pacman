import pygame
from .entity import Entity


class Pacman(Entity):
    def __init__(self, pos, moove, coord, sprite, player: int):
        super().__init__(pos, moove, coord, sprite)
        self.player = player
        self.score = 0

    def eat_pacgum(self, map):
        s_x, s_y = self.pos
        if map[s_x][s_y] == "p":
            self.score += 10
            map[s_x][s_y] = "*"

    def event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if self.player == 1:
                match event.key:
                    case pygame.K_RIGHT:
                        self.moove = (3, 0)
                    case pygame.K_LEFT:
                        self.moove = (-3, 0)
                    case pygame.K_DOWN:
                        self.moove = (0, 3)
                    case pygame.K_UP:
                        self.moove = (0, -3)
            else:
                match event.key:
                    case pygame.K_d:
                        self.moove = (3, 0)
                    case pygame.K_a:
                        self.moove = (-3, 0)
                    case pygame.K_s:
                        self.moove = (0, 3)
                    case pygame.K_w:
                        self.moove = (0, -3)

    def draw(self, surface: pygame.Surface):
        if isinstance(self.surface, pygame.Rect):
            if self.player == 1:
                pygame.draw.rect(surface, "white", self.surface)
            else:
                pygame.draw.rect(surface, "red", self.surface)
            print("ici")
        else:
            surface.blit(self.surface, self.coord)
