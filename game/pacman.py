import pygame
from entity import Entity


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

    def get_event(self, event: pygame.event.Event):
        match event.key:
            case pygame.K_RIGHT:
                self.moove = (1, 0)
            case pygame.K_LEFT:
                self.moove = (-1, 0)
            case pygame.K_DOWN:
                self.moove = (0, 1)
            case pygame.K_UP:
                self.moove = (0, -1)
