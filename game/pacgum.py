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
        score: int
    ):
        super().__init__(pos, moove, coord, sprite)
        self.score = score
        self.taken = False

    def draw(self, surface: pygame.Surface):
        if not self.taken:
            if isinstance(self.surface, pygame.Rect):
                pygame.draw.rect(surface, "lightblue", self.surface)
            else:
                surface.blit(self.surface, self.coord)

    def event(self, event): ...
