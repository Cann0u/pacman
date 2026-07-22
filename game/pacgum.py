from .entity import Entity
from typing import Tuple
import pygame


class PacGum(Entity):
    def __init__(
        self,
        pos: Tuple,
        moove: Tuple,
        coord: Tuple,
        sprite: pygame.Surface,
        score: int,
        hitbox
    ):
        super().__init__(pos, moove, coord, sprite, hitbox)
        self.score = score
        self.taken = False
        x, y = self.pos
        c_x, c_y = self.coord
        self.coord = x * 20 + c_x + 6, y * 20 + c_y + 6

    def draw(self, surface: pygame.Surface):
        if not self.taken:
            if isinstance(self.surface, pygame.Rect):
                pygame.draw.rect(surface, "white", self.surface)
            else:
                surface.blit(self.surface, self.coord)

    def event(self, event): ...
