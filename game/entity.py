from typing import Tuple, List
import pygame


class Entity:
    def __init__(
        self, pos: Tuple, moove: Tuple, coord: Tuple, sprite: pygame.Surface
    ):
        self.pos = pos
        self.coord = coord
        self.surface = sprite
        self.moove = moove

    def check_collapse(self, entity: List): ...

    def moove_on(self):
        p_x, p_y = self.coord
        d_x, d_y = self.moove
        w_x, w_y = pygame.display.get_window_size()
        if p_x + d_x < 0:
            self.coord = 0, d_y + p_y
        elif p_y + d_y < 0:
            self.coord = d_x + p_x, 0
        else:
            self.coord = d_x + p_x, d_y + p_y
        if isinstance(self.surface, pygame.Rect):
            self.surface.left, self.surface.top = self.coord

    def draw(self, surface):
        ...

    def event(self, event):
        ...
