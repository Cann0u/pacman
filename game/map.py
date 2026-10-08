from typing import List
from .entity import Entity
import pygame
from render import sprites


class Wall(Entity):
    def __init__(self, pos, moove, coord, sprite, hitbox):
        super().__init__(pos, moove, coord, sprite, hitbox)

    def draw(self, surface):
        if isinstance(self.surface, pygame.Rect):
            pygame.draw.rect(surface, "lightblue", self.surface)
        else:
            surface.blit(self.surface, self.coord)


class Map:
    def __init__(self, maze: List[List[str]]):
        self.maze = maze
        self.entity = []
        w_x, w_y = pygame.display.get_window_size()
        self.start = (
            w_x / 2 - len(self.maze[0]) / 2 * 20,
            w_y / 2 - len(self.maze) / 2 * 20,
        )

    def create(self):
        s_x, s_y = self.start
        for i, line in enumerate(self.maze):
            for j, col in enumerate(line):
                if col == "#":
                    sprite = None
                    if sprites.tiles_available():
                        sprite = sprites.wall_sprite(
                            self._is_wall(i - 1, j),
                            self._is_wall(i + 1, j),
                            self._is_wall(i, j - 1),
                            self._is_wall(i, j + 1),
                            self._is_wall(i - 1, j - 1),
                            self._is_wall(i - 1, j + 1),
                            self._is_wall(i + 1, j - 1),
                            self._is_wall(i + 1, j + 1),
                        )
                    self.entity.append(
                        Wall(
                            (i, j),
                            (0, 0),
                            (j * 20 + s_x, i * 20 + s_y),
                            sprite,
                            (20, 20),
                        )
                    )

    def _is_wall(self, i: int, j: int) -> bool:
        return (
            0 <= i < len(self.maze)
            and 0 <= j < len(self.maze[i])
            and self.maze[i][j] == "#"
        )
