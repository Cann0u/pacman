from typing import List
from .entity import Entity
import pygame


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
                    self.entity.append(
                        Wall(
                            (i, j),
                            (0, 0),
                            (j * 20 + s_x, i * 20 + s_y),
                            None,
                            (20, 20),
                        )
                    )
