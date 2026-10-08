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

TILESET_PATH = "sprite/tileset.png"
TILE_ORIGIN = (225, 0)
TILE_PITCH = 9
TILE = 8
CELL_PX = 20

_tileset = None
_tile_cache = {}


def _load_tileset():
    global _tileset
    if _tileset is None:
        try:
            img = pygame.image.load(TILESET_PATH).convert()
            img.set_colorkey((0, 0, 0))
            _tileset = img
        except (pygame.error, FileNotFoundError) as e:
            print(f"Tileset introuvable ({TILESET_PATH}) : {e}")
            _tileset = False
    return _tileset or None


def tiles_available() -> bool:
    return _load_tileset() is not None


def tile(col: int, row: int, size: int = TILE) -> pygame.Surface:
    key = ("tile", col, row, size)
    if key not in _tile_cache:
        rect = pygame.Rect(
            TILE_ORIGIN[0] + col * TILE_PITCH,
            TILE_ORIGIN[1] + row * TILE_PITCH,
            TILE,
            TILE,
        )
        t = _load_tileset().subsurface(rect).copy()
        if size != TILE:
            t = pygame.transform.scale(t, (size, size))
        t.set_colorkey((0, 0, 0))
        _tile_cache[key] = t
    return _tile_cache[key]


PELLET_TILE = (13, 5)
SUPER_PELLET_TILE = (15, 5)
SUPER_BLINK_MS = 250


def pacgum_sprite() -> pygame.Surface:
    return tile(*PELLET_TILE, size=16)


def super_pacgum_sprite():
    if (pygame.time.get_ticks() // SUPER_BLINK_MS) % 2:
        return None
    return tile(*SUPER_PELLET_TILE, size=12)

def _pad_tile(col: int, row: int) -> pygame.Surface:
    t = tile(col, row, size=16)
    canvas = pygame.Surface((CELL_PX, CELL_PX))
    canvas.fill((0, 0, 0))
    canvas.blit(t, (3, 3))
    scale = pygame.transform.scale
    canvas.blit(scale(t.subsurface((0, 0, 16, 1)), (16, 3)), (3, 0))
    canvas.blit(scale(t.subsurface((0, 15, 16, 1)), (16, 1)), (3, 19))
    canvas.blit(scale(t.subsurface((0, 0, 1, 16)), (3, 16)), (0, 3))
    canvas.blit(scale(t.subsurface((15, 0, 1, 16)), (1, 16)), (19, 3))
    for (cx, cy, w, h), px in (
        ((0, 0, 3, 3), (0, 0)),
        ((19, 0, 1, 3), (15, 0)),
        ((0, 19, 3, 1), (0, 15)),
        ((19, 19, 1, 1), (15, 15)),
    ):
        canvas.fill(t.get_at(px), (cx, cy, w, h))
    canvas.set_colorkey((0, 0, 0))
    return canvas


def _wall_pieces():
    if "pieces" not in _tile_cache:
        h = _pad_tile(4, 4)
        v = _pad_tile(8, 4)
        rd = _pad_tile(2, 5)
        flip = pygame.transform.flip
        _tile_cache["pieces"] = {
            "h": h,
            "v": v,
            ("right", "down"): rd,
            ("right", "up"): flip(rd, False, True),
            ("left", "down"): flip(rd, True, False),
            ("left", "up"): flip(rd, True, True),
        }
    return _tile_cache["pieces"]


def wall_sprite(up: bool, down: bool, left: bool, right: bool):
    key = ("wall", up, down, left, right)
    if key in _tile_cache:
        return _tile_cache[key]
    p = _wall_pieces()
    s = pygame.Surface((CELL_PX, CELL_PX))
    s.fill((0, 0, 0))
    n = up + down + left + right
    if n == 2 and (up or down) and (left or right):
        s.blit(p[("right" if right else "left", "down" if down else "up")], (0, 0))
    else:
        if up and down:
            s.blit(p["v"], (0, 0))
        elif up:
            s.blit(p["v"], (0, 0), (0, 0, CELL_PX, CELL_PX // 2 + 1))
        elif down:
            s.blit(p["v"], (0, CELL_PX // 2 - 1), (0, CELL_PX // 2 - 1, CELL_PX, CELL_PX // 2 + 1))
        if left and right:
            s.blit(p["h"], (0, 0))
        elif left:
            s.blit(p["h"], (0, 0), (0, 0, CELL_PX // 2 + 1, CELL_PX))
        elif right:
            s.blit(p["h"], (CELL_PX // 2 - 1, 0), (CELL_PX // 2 - 1, 0, CELL_PX // 2 + 1, CELL_PX))
        if n == 0:
            s.fill((33, 33, 255), (8, 8, 4, 4))
    s.set_colorkey((0, 0, 0))
    _tile_cache[key] = s
    return s