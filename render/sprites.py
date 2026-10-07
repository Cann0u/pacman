import pygame

SHEET_PATH = "sprite/spritesheet.png"
ORIGIN = (457, 1)
CELL = 16
INNER = 14

PACMAN_ROW = {"right": 0, "left": 1, "up": 2, "down": 3}
PACMAN_CYCLE = (0, 1, 2, 1)
PACMAN_FRAME_MS = 60

GHOST_FIRST_ROW = 4
GHOST_DIR_COL = {"right": 0, "left": 2, "up": 4, "down": 6}
GHOST_FRAME_MS = 150

FRIGHT_BLUE_COL = 8
FRIGHT_WHITE_COL = 10
FLASH_MS = 200

EYES_ROW = 5
EYES_DIR_COL = {"right": 8, "left": 9, "up": 10, "down": 11}

_sheet = None
_cache = {}


def _load_sheet():
    global _sheet
    if _sheet is None:
        try:
            img = pygame.image.load(SHEET_PATH).convert()
            img.set_colorkey((0, 0, 0))
            _sheet = img
        except (pygame.error, FileNotFoundError) as e:
            print(f"Spritesheet introuvable ({SHEET_PATH}) : {e}")
            _sheet = False
    return _sheet or None


def available() -> bool:
    return _load_sheet() is not None


def get(col: int, row: int, size: int = CELL, recolor=None) -> pygame.Surface:
    key = (col, row, size, recolor)
    if key not in _cache:
        sheet = _load_sheet()
        rect = pygame.Rect(
            ORIGIN[0] + col * CELL, ORIGIN[1] + row * CELL, INNER, INNER
        )
        sprite = pygame.Surface((CELL, CELL))
        sprite.fill((0, 0, 0))
        sprite.blit(sheet.subsurface(rect), (1, 1))
        if recolor:
            old, new = recolor
            for x in range(CELL):
                for y in range(CELL):
                    if sprite.get_at((x, y))[:3] == old:
                        sprite.set_at((x, y), new)
        if size != CELL:
            sprite = pygame.transform.scale(sprite, (size, size))
        sprite.set_colorkey((0, 0, 0))
        _cache[key] = sprite
    return _cache[key]


def direction_from_move(move, default):
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


def pacman_frame(direction: str, moving: bool, player: int = 1):
    if moving:
        step = (pygame.time.get_ticks() // PACMAN_FRAME_MS) % len(PACMAN_CYCLE)
        col = PACMAN_CYCLE[step]
    else:
        col = 1
    recolor = None if player == 1 else ((255, 255, 0), (0, 255, 255))
    return get(col, PACMAN_ROW[direction], recolor=recolor)


def ghost_frame(ghost: int, direction: str, frightened: bool, flash: bool,
                ate: bool):
    t = pygame.time.get_ticks()
    anim = (t // GHOST_FRAME_MS) % 2
    if ate:
        return get(EYES_DIR_COL[direction], EYES_ROW)
    if frightened:
        white = flash and (t // FLASH_MS) % 2 == 1
        base = FRIGHT_WHITE_COL if white else FRIGHT_BLUE_COL
        return get(base + anim, GHOST_FIRST_ROW)
    return get(GHOST_DIR_COL[direction] + anim, GHOST_FIRST_ROW + ghost - 1)