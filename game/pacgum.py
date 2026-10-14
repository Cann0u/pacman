from .entity import Entity
from typing import Tuple
import pygame


class PacGum(Entity):
    def __init__(
        self,
        pos: Tuple[int, int],
        moove: Tuple[int, int],
        coord: Tuple[float, float],
        sprite: pygame.Surface,
        score: int,
        hitbox:Tuple[int, int, int, int],
    ):
        super().__init__(pos, moove, coord, sprite, hitbox)
        self.score = score
        self.taken = False

    def draw(self, surface: pygame.Surface) -> None:
        if not self.taken:
            if isinstance(self.surface, pygame.Rect):
                pygame.draw.rect(surface, "white", self.surface)
            else:
                surface.blit(self.surface, self.coord)

    def event(self, event: pygame.event.Event) -> None: ...
