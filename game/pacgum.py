from .entity import Entity
import pygame
from render.sprites import Sprites


class PacGum(Entity):
    def __init__(
        self,
        pos: tuple[int, int],
        moove: tuple[int, int],
        coord: tuple[float, float],
        score: int,
        hitbox: tuple[int, int],
        sprites: Sprites,
    ) -> None:
        super().__init__(pos, moove, coord, hitbox)
        self.score = score
        self.taken = False
        self.sprites = sprites

    def draw(self, surface: pygame.surface.Surface) -> None:
        if not self.taken:
            if self.sprites.tiles_available():
                surface.blit(
                    self.sprites.pacgum_sprite(),
                    (self.coord[0] - 4, self.coord[1] - 4),
                )
            else:
                pygame.draw.rect(surface, "white", self.surface)

    def event(
        self, event: pygame.event.Event, entity: list[Entity] | None = None
    ) -> None: ...


class SuperPacGum(Entity):
    def __init__(
        self,
        pos: tuple[int, int],
        moove: tuple[int, int],
        coord: tuple[float, float],
        score: int,
        hitbox: tuple[int, int],
        sprites: Sprites,
    ) -> None:
        super().__init__(pos, moove, coord, hitbox)
        self.score = score
        self.taken = False
        self.sprites = sprites

    def draw(self, surface: pygame.surface.Surface) -> None:
        if not self.taken:
            if self.sprites.tiles_available():
                frame = self.sprites.super_pacgum_sprite()
                if frame:
                    surface.blit(frame, self.coord)
            else:
                pygame.draw.rect(surface, "red", self.surface)

    def event(
        self, event: pygame.event.Event, entity: list[Entity] | None = None
    ) -> None: ...
