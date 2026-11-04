import pygame
from .entity import Entity
from .map import Wall
from render.sprites import Sprites


class Pacman(Entity):
    def __init__(
        self,
        pos: tuple[int, int],
        moove: tuple[int, int],
        coord: tuple[float, float],
        player: int,
        font: pygame.font.Font,
        hitbox: tuple[int, int],
        live: int,
        score: int,
        sprites: Sprites,
    ) -> None:
        super().__init__(pos, moove, coord, hitbox, speed=1)
        self.player = player
        self.score = score
        self.font = font
        x, y = self.pos
        self.spawn: tuple[int, int] = x, y
        c_x, c_y = self.coord
        self.coord = x * 20 + c_x + 2, y * 20 + c_y + 2
        self.live = live
        self.next: tuple[int, int] = (0, 0)
        self.hit_ghost = False
        self.frightened_mode = False
        self.frightened_start: int | None = None
        self.ghost_multiplier = 1
        self.cheat = False
        self.facing = "right"
        self.death_start: int | None = None
        self.surface.topleft = (int(self.coord[0]), int(self.coord[1]))
        self.sprites = sprites

    def eat_pacgum(self, map: list[list[str]]) -> None:
        s_x, s_y = self.pos
        if map[s_x][s_y] == "p":
            self.score += 10
            map[s_x][s_y] = "*"

    def event(
        self, event: pygame.event.Event, entity: list[Entity] | None = None
    ) -> None:
        if entity is None:
            entity = []
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_c:
                    self.cheat = not self.cheat
                case pygame.K_p:
                    self.live += 1
            if self.player == 2:
                match event.key:
                    case pygame.K_RIGHT:
                        m_x, m_y = self.moove
                        prev = m_x, m_y
                        self.moove = (2, 0)
                        ent = self.check_collapse(entity)
                        if isinstance(ent, Wall):
                            self.moove = prev
                        self.next = (2, 0)
                    case pygame.K_LEFT:
                        prev = m_x, m_y = self.moove
                        self.moove = (-2, 0)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (-2, 0)
                    case pygame.K_DOWN:
                        prev = m_x, m_y = self.moove
                        self.moove = (0, 2)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (0, 2)
                    case pygame.K_UP:
                        prev = m_x, m_y = self.moove
                        self.moove = (0, -2)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (0, -2)
            else:
                match event.key:
                    case pygame.K_d:
                        prev = m_x, m_y = self.moove
                        self.moove = (2, 0)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (2, 0)
                    case pygame.K_a:
                        prev = m_x, m_y = self.moove
                        self.moove = (-2, 0)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (-2, 0)
                    case pygame.K_s:
                        prev = m_x, m_y = self.moove
                        self.moove = (0, 2)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (0, 2)
                    case pygame.K_w:
                        prev = m_x, m_y = self.moove
                        self.moove = (0, -2)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (0, -2)

    def check_next(self, entity: list[Entity]) -> None:
        m_x, m_y = self.moove
        prev = m_x, m_y
        m_x, m_y = self.next
        next = m_x, m_y
        if m_x != 0 or m_y != 0:
            self.moove = next
            ent = self.check_collapse(entity)
            if isinstance(ent, Pacman) or isinstance(ent, Wall):
                self.moove = prev

    def check_entity(self, entity: list[Entity]) -> None:
        ent = self.check_collapse(entity)
        from .pacgum import PacGum, SuperPacGum
        from .ghosts import Ghost

        if isinstance(ent, PacGum):
            self.score += ent.score
            ent.taken = True
        if isinstance(ent, SuperPacGum):
            self.score += ent.score
            ent.taken = True
            self.frightened_mode = True
            self.ghost_multiplier = 1
            self.frightened_start = pygame.time.get_ticks()
        if isinstance(ent, Ghost):
            if ent.frightened and not ent.ate:
                self.score += 200 * self.ghost_multiplier
                self.ghost_multiplier += 1
                ent.ate = True

                ent.speed = ent.base_speed * 3
            elif not self.cheat and not ent.ate:
                self.live -= 1
                self.hit_ghost = True
        if isinstance(ent, Pacman) or isinstance(ent, Wall):
            self.moove = 0, 0

    def draw(self, surface: pygame.surface.Surface) -> None:
        if self.live <= 0 and self.death_start is None:
            return
        if self.sprites.available():
            if self.death_start is not None:
                elapsed = pygame.time.get_ticks() - self.death_start
                frame = self.sprites.pacman_death_frame(
                    elapsed, self.facing, self.player
                )
                if frame:
                    surface.blit(frame, self.coord)
            else:
                self.facing = self.sprites.direction_from_move(
                    self.moove, self.facing
                )
                moving = self.moove != (0, 0)
                frame = self.sprites.pacman_frame(
                    self.facing, moving, self.player
                )
                surface.blit(frame, self.coord)
        elif self.player == 1:
            pygame.draw.rect(surface, "yellow", self.surface)
        else:
            pygame.draw.rect(surface, "darkblue", self.surface)
        w_x, w_y = pygame.display.get_window_size()
        if self.player == 1:
            width = 10
        else:
            width = 90
        w, height = self.font.size("live: " + str(self.live))
        surface.blit(
            self.font.render("live: " + str(self.live), False, "white"),
            (w_x / (100 / width) - w / 2, 0),
        )
        surface.blit(
            self.font.render(str(self.score), False, "white"),
            (w_x / (100 / width), height + height / 2),
        )
