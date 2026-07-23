from .entity import Entity
from .algo import Algo

DIRECTION_TO_MOOVE = {
    "up": (0, -2),
    "down": (0, 2),
    "left": (-2, 0),
    "right": (2, 0),
}


class Ghost(Entity):
    def __init__(self, pos, coord, sprite, ghost: int, algo: Algo, hitbox=(16, 16)):
        super().__init__(pos, (0, 0), coord, sprite, hitbox)
        self.ghost = ghost
        self.algo = algo
        self.direction = None

    def update_target(self, target_pos):
        direction = self.algo.next_move(self.pos, target_pos, self.direction)
        if direction:
            self.direction = direction
            self.moove = DIRECTION_TO_MOOVE[direction]

    def draw(self, surface):
        import pygame
        if isinstance(self.surface, pygame.Rect):
            pygame.draw.rect(surface, "red", self.surface)
        else:
            surface.blit(self.surface, self.coord)