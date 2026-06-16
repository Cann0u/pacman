from typing import Tuple
import pygame


class Entity:
    def __init__(self, pos: Tuple, sprite: pygame.Surface):
        self.pos = pos
        self.surface = sprite

    def check_collapse(self):
        ...

    def moove(self, dir: Tuple):
        p_x, p_y = self.pos
        d_x, d_y = dir
        self.pos = d_x + p_x, d_y + p_y
