from typing import Tuple
import pygame


class Entity:
    def __init__(
        self, pos: Tuple, moove: Tuple, coord: Tuple, sprite: pygame.Surface
    ):
        self.pos = pos
        self.coord = coord
        self.surface = sprite
        self.moove = moove

    def check_collapse(self): ...

    def moove_on(self):
        p_x, p_y = self.pos
        d_x, d_y = self.moove
        self.pos = d_x + p_x, d_y + p_y
