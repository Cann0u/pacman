import pygame

from .entity import Entity
from .algo import Algo
from typing import List, Tuple

DIRECTION_TO_MOOVE = {
    "up": (0, -2),
    "down": (0, 2),
    "left": (-2, 0),
    "right": (2, 0),
}

BLINKY, PINKY, INKY, CLYDE = 1, 2, 3, 4


class Ghost(Entity):
    def __init__(
        self,
        pos: Tuple[int, int],
        coord: Tuple[int, int],
        sprite: pygame.Surface,
        ghost: int,
        algo: Algo,
        hitbox: Tuple[int, int]=(16, 16),
        speed: float=1.0,
    ):
        super().__init__(pos, (0, 0), coord, sprite, hitbox)
        self.ghost = ghost
        self.algo = algo
        self.direction: str | None = None
        self.spawn = pos
        self.speed = speed
        self.move_accumulator = 0.0

    def compute_target(self, pacman_pos: Tuple[int, int], pacman_dir: Tuple[int, int], ghosts: List["Ghost"]) -> Tuple[int, int]:
        p_x, p_y = pacman_pos
        d_x, d_y = pacman_dir

        if self.ghost == BLINKY:
            return pacman_pos

        if self.ghost == PINKY:
            return p_x + d_x * 4, p_y + d_y * 4

        if self.ghost == INKY:
            ahead_x, ahead_y = p_x + d_x * 2, p_y + d_y * 2
            blinky: Ghost | None = next((g for g in ghosts if g.ghost == BLINKY), None)
            if not blinky:
                return pacman_pos
            b_x, b_y = blinky.pos
            return ahead_x + (ahead_x - b_x), ahead_y + (ahead_y - b_y)

        if self.ghost == CLYDE:
            g_x, g_y = self.pos
            if (g_x - p_x) ** 2 + (g_y - p_y) ** 2 > 64:
                return pacman_pos
            maze = self.algo.map.maze
            return len(maze[0]) - 2, len(maze) - 2

        return pacman_pos

    def update_target(self, pacman_pos: Tuple[int, int], pacman_dir: Tuple[int, int]=(0, 0), ghosts: List["Ghost"] | None = None) -> None:
        target = self.compute_target(pacman_pos, pacman_dir, ghosts or [])
        direction = self.algo.next_move(self.pos, target)
        if direction:
            self.direction = direction
            self.moove = DIRECTION_TO_MOOVE[direction]

    def draw(self, surface: pygame.Surface) -> None:
        import pygame

        colors = {BLINKY: "red", PINKY: "pink", INKY: "cyan", CLYDE: "orange"}
        if isinstance(self.surface, pygame.Rect):
            pygame.draw.rect(
                surface, colors.get(self.ghost, "red"), self.surface
            )
        else:
            surface.blit(self.surface, self.coord)

    def event(self, event: pygame.event.Event) -> None: ...