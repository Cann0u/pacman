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


def _recolor(sprite: pygame.Surface, old, new) -> None:
    for x in range(sprite.get_width()):
        for y in range(sprite.get_height()):
            if sprite.get_at((x, y))[:3] == old:
                sprite.set_at((x, y), new)


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
            _recolor(sprite, *recolor)
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


def ghost_frame(
    ghost: int, direction: str, frightened: bool, flash: bool, ate: bool
):
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


LOGICAL = 10
LINE_A = 2
LINE_B = 7
PX = CELL_PX // LOGICAL


def _wall_pixels(up, down, left, right, ul, ur, dl, dr):
    px = set()
    A, B, END = LINE_A, LINE_B, LOGICAL - 1

    x0 = 0 if left else 4
    x1 = END if right else 5
    y0 = 0 if up else 4
    y1 = END if down else 5
    if not up:
        px.update((x, A) for x in range(x0, x1 + 1))
    if not down:
        px.update((x, B) for x in range(x0, x1 + 1))
    if not left:
        px.update((A, y) for y in range(y0, y1 + 1))
    if not right:
        px.update((B, y) for y in range(y0, y1 + 1))

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
    up, down, left, right, up_left, up_right, down_left, down_right
):
    key = (
        "wall",
        up,
        down,
        left,
        right,
        up_left,
        up_right,
        down_left,
        down_right,
    )
    if key not in _tile_cache:
        color = tile(4, 4).get_at((0, 3))[:3]
        surf = pygame.Surface((CELL_PX, CELL_PX))
        surf.fill((0, 0, 0))
        for x, y in _wall_pixels(*key[1:]):
            surf.fill(color, (x * PX, y * PX, PX, PX))
        surf.set_colorkey((0, 0, 0))
        _tile_cache[key] = surf
    return _tile_cache[key]


DEATH_COLS = tuple(range(3, 14))
DEATH_FREEZE_MS = 150
DEATH_FRAME_MS = 150
DEATH_END_PAUSE_MS = 400
DEATH_TOTAL_MS = (
    DEATH_FREEZE_MS + len(DEATH_COLS) * DEATH_FRAME_MS + DEATH_END_PAUSE_MS
)
PLAYER2_RECOLOR = ((255, 255, 0), (0, 255, 255))


def death_duration() -> int:
    return DEATH_TOTAL_MS


def death_hides_ghosts(elapsed: int) -> bool:
    return elapsed >= DEATH_FREEZE_MS


def _death_sprite(col: int, recolor=None) -> pygame.Surface:
    key = ("death", col, recolor)
    if key not in _cache:
        height = 15 if col == DEATH_COLS[-1] else 14
        rect = pygame.Rect(ORIGIN[0] + col * CELL - 1, ORIGIN[1], CELL, height)
        sprite = pygame.Surface((CELL, CELL))
        sprite.fill((0, 0, 0))
        sprite.blit(_load_sheet().subsurface(rect), (0, 1))
        if recolor:
            _recolor(sprite, *recolor)
        sprite.set_colorkey((0, 0, 0))
        _cache[key] = sprite
    return _cache[key]


def pacman_death_frame(elapsed: int, direction: str, player: int = 1):
    if elapsed < DEATH_FREEZE_MS:
        return pacman_frame(direction, False, player)
    index = (elapsed - DEATH_FREEZE_MS) // DEATH_FRAME_MS
    if index >= len(DEATH_COLS):
        return None
    recolor = None if player == 1 else PLAYER2_RECOLOR
    return _death_sprite(DEATH_COLS[index], recolor)
