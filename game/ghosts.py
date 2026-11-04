from __future__ import annotations

import pygame

from .entity import Entity
from .algo import Algo
from render.sprites import Sprites

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
        pos: tuple[int, int],
        coord: tuple[float, float],
        ghost: int,
        algo: Algo,
        sprites: Sprites,
        hitbox: tuple[int, int] = (16, 16),
        speed: float = 1.0,
    ) -> None:
        super().__init__(pos, (0, 0), coord, hitbox, speed)
        self.ghost = ghost
        self.algo = algo
        self.direction: str | None = None
        self.spawn = pos
        self.base_speed = speed
        self.move_accumulator = 0.0
        self.frightened = False
        self.ate = False
        self.flash = False
        self.sprites = sprites

    def compute_target(
        self,
        pacman_pos: tuple[int, int],
        pacman_dir: tuple[int, int],
        ghosts: list[Ghost],
    ) -> tuple[int, int]:
        p_x, p_y = pacman_pos
        d_x, d_y = pacman_dir

        if self.ghost == BLINKY:
            return pacman_pos

        if self.ghost == PINKY:
            g_x, g_y = self.pos
            if (g_x - p_x) ** 2 + (g_y - p_y) ** 2 < 16:
                return pacman_pos
            return p_x + d_x * 4, p_y + d_y * 4

        if self.ghost == INKY:
            ahead_x, ahead_y = p_x + d_x * 2, p_y + d_y * 2
            blinky = next((g for g in ghosts if g.ghost == BLINKY), None)
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

    def update_target(
        self,
        pacman_pos: tuple[int, int] = (0, 0),
        pacman_dir: tuple[int, int] = (0, 0),
        ghosts: list[Ghost] | None = None,
    ) -> None:
        if self.ate:
            target = self.spawn
        elif self.frightened:
            target = self.algo.flee_target(self.pos, pacman_pos)
        else:
            target = self.compute_target(pacman_pos, pacman_dir, ghosts or [])
        direction = self.algo.next_move(self.pos, target)
        if direction:
            self.direction = direction
            self.moove = DIRECTION_TO_MOOVE[direction]

    def draw(self, surface: pygame.surface.Surface) -> None:
        import pygame

        if self.sprites.available():
            frame = self.sprites.ghost_frame(
                self.ghost,
                self.direction or "left",
                self.frightened,
                self.flash,
                self.ate,
            )
            surface.blit(frame, self.coord)
            return

        colors = {BLINKY: "red", PINKY: "pink", INKY: "cyan", CLYDE: "orange"}
        if self.ate:
            color = "white"
        elif self.frightened:
            color = "blue"
        else:
            color = colors.get(self.ghost, "red")
        pygame.draw.rect(surface, color, self.surface)
