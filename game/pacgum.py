from .entity import Entity
from typing import Tuple
import pygame
from render import sprites


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

    def draw(self, surface: pygame.Surface):
        if not self.taken:
            if sprites.tiles_available():
                surface.blit(
                    sprites.pacgum_sprite(),
                    (self.coord[0] - 4, self.coord[1] - 4),
                )
            elif isinstance(self.surface, pygame.Rect):
                pygame.draw.rect(surface, "white", self.surface)
            else:
                surface.blit(self.surface, self.coord)

    def event(self, event): ...


class SuperPacGum(Entity):
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

    def draw(self, surface: pygame.Surface):
        if not self.taken:
            if sprites.tiles_available():
                frame = sprites.super_pacgum_sprite()
                if frame:
                    surface.blit(frame, self.coord)
            elif isinstance(self.surface, pygame.Rect):
                pygame.draw.rect(surface, "red", self.surface)
            else:
                surface.blit(self.surface, self.coord)

    def event(self, event): ...