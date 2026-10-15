import pygame
from .entity import Entity
from .map import Wall
from typing import List, Tuple


class Pacman(Entity):
    def __init__(
        self,
        pos: Tuple[int, int],
        moove: Tuple[int, int],
        coord: Tuple[float, float],
        sprite: pygame.Surface,
        player: int,
        font: pygame.font.Font,
        hitbox: Tuple[int, int],
        live: int,
        score: int
    ):
        super().__init__(pos, moove, coord, sprite, hitbox)
        self.player = player
        self.score = score
        self.font = font
        x, y = self.pos
        self.spawn = x, y
        c_x, c_y = self.coord
        self.coord = x * 20 + c_x + 2, y * 20 + c_y + 2
        self.live = live
        self.next = (0, 0)
        self.hit_ghost = False
        self.cheat = False
        if not sprite:
            self.surface = pygame.Rect(self.coord, self.hitbox)
        else:
            self.surface = sprite

    def eat_pacgum(self, game_map: List[List[str]]) -> None:
        s_x, s_y = self.pos
        if game_map[s_x][s_y] == "p":
            self.score += 10
            game_map[s_x][s_y] = "*"

    def event(self, event: pygame.event.Event, entity: List[Entity] | None = None) -> None:
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
                        prev = self.moove
                        self.moove = (-2, 0)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (-2, 0)
                    case pygame.K_DOWN:
                        prev = self.moove
                        self.moove = (0, 2)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (0, 2)
                    case pygame.K_UP:
                        prev = self.moove
                        self.moove = (0, -2)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (0, -2)
            else:
                match event.key:
                    case pygame.K_d:
                        prev = self.moove
                        self.moove = (2, 0)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (2, 0)
                    case pygame.K_a:
                        prev = self.moove
                        self.moove = (-2, 0)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (-2, 0)
                    case pygame.K_s:
                        prev = self.moove
                        self.moove = (0, 2)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (0, 2)
                    case pygame.K_w:
                        prev = self.moove
                        self.moove = (0, -2)
                        ent = self.check_collapse(entity)
                        if ent:
                            self.moove = prev
                        self.next = (0, -2)

    def check_next(self, entity: List[Entity]) -> None:
        m_x, m_y = self.moove
        prev = m_x, m_y
        m_x, m_y = self.next
        next_move = m_x, m_y
        if m_x != 0 or m_y != 0:
            self.moove = next_move
            ent = self.check_collapse(entity)
            if isinstance(ent, Pacman) or isinstance(ent, Wall):
                self.moove = prev

    def check_entity(self, entity: List[Entity]) -> None:
        ent = self.check_collapse(entity)
        from .pacgum import PacGum
        from .ghosts import Ghost

        if isinstance(ent, PacGum):
            self.score += ent.score
            ent.taken = True
        if isinstance(ent, Ghost) and not self.cheat:
            self.live -= 1
            self.hit_ghost = True
        if isinstance(ent, Pacman) or isinstance(ent, Wall):
            self.moove = 0, 0

    def draw(self, surface: pygame.Surface) -> None:
        if self.live <= 0:
            return
        if isinstance(self.surface, pygame.Rect):
            if self.player == 1:
                pygame.draw.rect(surface, "yellow", self.surface)
            else:
                pygame.draw.rect(surface, "darkblue", self.surface)
        else:
            surface.blit(self.surface, self.coord)
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
