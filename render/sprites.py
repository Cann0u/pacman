from pathlib import Path
from typing import Optional

import pygame

Color = tuple[int, int, int]
Recolor = Optional[tuple[Color, Color]]

ASSETS = Path(__file__).resolve().parent.parent / "sprite"

CELL = 16
INNER = 14
ORIGIN = (457, 1)

PACMAN_ROW = {"right": 0, "left": 1, "up": 2, "down": 3}
PACMAN_CYCLE = (0, 1, 2, 1)
PACMAN_FRAME_MS = 60
PLAYER2_RECOLOR: tuple[Color, Color] = ((255, 255, 0), (0, 255, 255))

GHOST_FIRST_ROW = 4
GHOST_DIR_COL = {"right": 0, "left": 2, "up": 4, "down": 6}
GHOST_FRAME_MS = 150
FRIGHT_BLUE_COL = 8
FRIGHT_WHITE_COL = 10
FLASH_MS = 200
EYES_ROW = 5
EYES_DIR_COL = {"right": 8, "left": 9, "up": 10, "down": 11}

TILE_ORIGIN = (225, 0)
TILE_PITCH = 9
TILE = 8
CELL_PX = 20
PELLET_TILE = (13, 5)
SUPER_PELLET_TILE = (15, 5)
SUPER_BLINK_MS = 250

LOGICAL = 10
LINE_A = 2
LINE_B = 7
PX = CELL_PX // LOGICAL

DEATH_COLS = tuple(range(3, 14))
DEATH_FREEZE_MS = 150
DEATH_FRAME_MS = 150
DEATH_END_PAUSE_MS = 400
DEATH_TOTAL_MS = (
    DEATH_FREEZE_MS + len(DEATH_COLS) * DEATH_FRAME_MS + DEATH_END_PAUSE_MS
)


class Sprites:
    def __init__(
        self,
        sheet_path: Path = ASSETS / "spritesheet.png",
        tileset_path: Path = ASSETS / "tileset.png",
    ) -> None:
        self._sheet = self._load(sheet_path)
        self._tileset = self._load(tileset_path)
        self._cache: dict[tuple[object, ...], pygame.surface.Surface] = {}

    @staticmethod
    def _load(path: Path) -> Optional[pygame.surface.Surface]:
        try:
            img = pygame.image.load(str(path)).convert()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Image not found ({path}): {e}")
            return None
        img.set_colorkey((0, 0, 0))
        return img

    def available(self) -> bool:
        return self._sheet is not None

    def tiles_available(self) -> bool:
        return self._tileset is not None

    @staticmethod
    def _recolor(
        sprite: pygame.surface.Surface, old: Color, new: Color
    ) -> None:
        for x in range(sprite.get_width()):
            for y in range(sprite.get_height()):
                if tuple(sprite.get_at((x, y)))[:3] == old:
                    sprite.set_at((x, y), new)

    @staticmethod
    def direction_from_move(
        move: tuple[int, int], default: str
    ) -> str:
        dx, dy = move
        if dx > 0:
            return "right"
        if dx < 0:
            return "left"
        if dy > 0:
            return "down"
        if dy < 0:
            return "up"
        return default

    def _character(
        self, col: int, row: int, size: int = CELL, recolor: Recolor = None
    ) -> pygame.surface.Surface:
        key = ("char", col, row, size, recolor)
        if key not in self._cache:
            if self._sheet is None:
                raise RuntimeError("spritesheet not loaded")
            rect = pygame.Rect(
                ORIGIN[0] + col * CELL, ORIGIN[1] + row * CELL, INNER, INNER
            )
            sprite = pygame.surface.Surface((CELL, CELL))
            sprite.fill((0, 0, 0))
            sprite.blit(self._sheet.subsurface(rect), (1, 1))
            if recolor:
                self._recolor(sprite, *recolor)
            if size != CELL:
                sprite = pygame.transform.scale(sprite, (size, size))
            sprite.set_colorkey((0, 0, 0))
            self._cache[key] = sprite
        return self._cache[key]

    def pacman_frame(
        self, direction: str, moving: bool, player: int = 1
    ) -> pygame.surface.Surface:
        if moving:
            step = (
                pygame.time.get_ticks() // PACMAN_FRAME_MS
            ) % len(PACMAN_CYCLE)
            col = PACMAN_CYCLE[step]
        else:
            col = 1
        recolor = None if player == 1 else PLAYER2_RECOLOR
        return self._character(col, PACMAN_ROW[direction], recolor=recolor)

    def ghost_frame(
        self,
        ghost: int,
        direction: str,
        frightened: bool,
        flash: bool,
        ate: bool,
    ) -> pygame.surface.Surface:
        t = pygame.time.get_ticks()
        anim = (t // GHOST_FRAME_MS) % 2
        if ate:
            return self._character(EYES_DIR_COL[direction], EYES_ROW)
        if frightened:
            white = flash and (t // FLASH_MS) % 2 == 1
            base = FRIGHT_WHITE_COL if white else FRIGHT_BLUE_COL
            return self._character(base + anim, GHOST_FIRST_ROW)
        return self._character(
            GHOST_DIR_COL[direction] + anim, GHOST_FIRST_ROW + ghost - 1
        )

    @staticmethod
    def death_duration() -> int:
        return DEATH_TOTAL_MS

    @staticmethod
    def death_hides_ghosts(elapsed: int) -> bool:
        return elapsed >= DEATH_FREEZE_MS

    def _death_sprite(
        self, col: int, recolor: Recolor = None
    ) -> pygame.surface.Surface:
        key = ("death", col, recolor)
        if key not in self._cache:
            if self._sheet is None:
                raise RuntimeError("spritesheet not loaded")
            height = 15 if col == DEATH_COLS[-1] else 14
            rect = pygame.Rect(
                ORIGIN[0] + col * CELL - 1, ORIGIN[1], CELL, height
            )
            sprite = pygame.surface.Surface((CELL, CELL))
            sprite.fill((0, 0, 0))
            sprite.blit(self._sheet.subsurface(rect), (0, 1))
            if recolor:
                self._recolor(sprite, *recolor)
            sprite.set_colorkey((0, 0, 0))
            self._cache[key] = sprite
        return self._cache[key]

    def pacman_death_frame(
        self, elapsed: int, direction: str, player: int = 1
    ) -> Optional[pygame.surface.Surface]:
        if elapsed < DEATH_FREEZE_MS:
            return self.pacman_frame(direction, False, player)
        index = (elapsed - DEATH_FREEZE_MS) // DEATH_FRAME_MS
        if index >= len(DEATH_COLS):
            return None
        recolor = None if player == 1 else PLAYER2_RECOLOR
        return self._death_sprite(DEATH_COLS[index], recolor)

    def tile(
        self, col: int, row: int, size: int = TILE
    ) -> pygame.surface.Surface:
        key = ("tile", col, row, size)
        if key not in self._cache:
            if self._tileset is None:
                raise RuntimeError("tileset not loaded")
            rect = pygame.Rect(
                TILE_ORIGIN[0] + col * TILE_PITCH,
                TILE_ORIGIN[1] + row * TILE_PITCH,
                TILE,
                TILE,
            )
            t = self._tileset.subsurface(rect).copy()
            if size != TILE:
                t = pygame.transform.scale(t, (size, size))
            t.set_colorkey((0, 0, 0))
            self._cache[key] = t
        return self._cache[key]

    def pacgum_sprite(self) -> pygame.surface.Surface:
        return self.tile(*PELLET_TILE, size=16)

    def super_pacgum_sprite(self) -> Optional[pygame.surface.Surface]:
        if (pygame.time.get_ticks() // SUPER_BLINK_MS) % 2:
            return None
        return self.tile(*SUPER_PELLET_TILE, size=12)

    @staticmethod
    def _wall_pixels(
        up: bool, down: bool, left: bool, right: bool,
        ul: bool, ur: bool, dl: bool, dr: bool,
    ) -> set[tuple[int, int]]:
        px: set[tuple[int, int]] = set()
        a, b, end = LINE_A, LINE_B, LOGICAL - 1

        x0 = 0 if left else 4
        x1 = end if right else 5
        y0 = 0 if up else 4
        y1 = end if down else 5
        if not up:
            px.update((x, a) for x in range(x0, x1 + 1))
        if not down:
            px.update((x, b) for x in range(x0, x1 + 1))
        if not left:
            px.update((a, y) for y in range(y0, y1 + 1))
        if not right:
            px.update((b, y) for y in range(y0, y1 + 1))

        if not up and not left:
            px.add((3, 3))
        if not up and not right:
            px.add((6, 3))
        if not down and not left:
            px.add((3, 6))
        if not down and not right:
            px.add((6, 6))

        if up and left and not ul:
            px.update({(2, 0), (2, 1), (1, 2), (0, 2)})
        if up and right and not ur:
            px.update({(7, 0), (7, 1), (8, 2), (9, 2)})
        if down and left and not dl:
            px.update({(2, 9), (2, 8), (1, 7), (0, 7)})
        if down and right and not dr:
            px.update({(7, 9), (7, 8), (8, 7), (9, 7)})
        return px

    def wall_sprite(
        self,
        up: bool, down: bool, left: bool, right: bool,
        up_left: bool, up_right: bool, down_left: bool, down_right: bool,
    ) -> pygame.surface.Surface:
        flags = (up, down, left, right,
                 up_left, up_right, down_left, down_right)
        key = ("wall", *flags)
        if key not in self._cache:
            c = self.tile(4, 4).get_at((0, 3))
            color: Color = (c[0], c[1], c[2])
            surf = pygame.surface.Surface((CELL_PX, CELL_PX))
            surf.fill((0, 0, 0))
            for x, y in self._wall_pixels(*flags):
                surf.fill(color, (x * PX, y * PX, PX, PX))
            surf.set_colorkey((0, 0, 0))
            self._cache[key] = surf
        return self._cache[key]
