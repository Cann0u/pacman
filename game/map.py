from typing import List, Tuple
from .entity import Entity
import pygame


class Wall(Entity):
    def __init__(
        self,
        pos: Tuple[int, int],
        moove: Tuple[int, int],
        coord: Tuple[float, float],
        sprite: pygame.Surface,
        hitbox: Tuple[int, int],
    ):
        super().__init__(pos, moove, coord, sprite, hitbox)

    def draw(self, surface: pygame.Surface) -> None:
        if isinstance(self.surface, pygame.Rect):
            pygame.draw.rect(surface, "lightblue", self.surface)
        else:
            surface.blit(self.surface, self.coord)

    def event(self, event: pygame.event.Event) -> None: ...


class Map:
    def __init__(self, maze: List[List[str]]):
        self.maze = maze
        self.entity: List[Entity] = []
        w_x, w_y = pygame.display.get_window_size()
        self.start = (
            w_x / 2 - len(self.maze[0]) / 2 * 20,
            w_y / 2 - len(self.maze) / 2 * 20,
        )

    def create(self) -> None:
        s_x, s_y = self.start
        for i, line in enumerate(self.maze):
            for j, col in enumerate(line):
                if col == "#":
                    self.entity.append(
                        Wall(
                            (i, j),
                            (0, 0),
                            (j * 20 + s_x, i * 20 + s_y),
                            None,
                            (20, 20),
                        )
                    )
