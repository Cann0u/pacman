import pygame
from .entity import Entity
from typing import List
from .pacgum import PacGum


class Pacman(Entity):
    def __init__(
        self, pos, moove, coord, sprite, player: int, font: pygame.font.Font
    ):
        super().__init__(pos, moove, coord, sprite)
        self.player = player
        self.score = 0
        self.font = font

    def eat_pacgum(self, map):
        s_x, s_y = self.pos
        if map[s_x][s_y] == "p":
            self.score += 10
            map[s_x][s_y] = "*"

    def event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if self.player == 1:
                match event.key:
                    case pygame.K_RIGHT:
                        self.moove = (2, 0)
                    case pygame.K_LEFT:
                        self.moove = (-2, 0)
                    case pygame.K_DOWN:
                        self.moove = (0, 2)
                    case pygame.K_UP:
                        self.moove = (0, -2)
            else:
                match event.key:
                    case pygame.K_d:
                        self.moove = (2, 0)
                    case pygame.K_a:
                        self.moove = (-2, 0)
                    case pygame.K_s:
                        self.moove = (0, 2)
                    case pygame.K_w:
                        self.moove = (0, -2)

    def check_collapse(self, entity: List[Entity]):
        x, y = self.coord
        m_x, m_y = self.moove
        x, y = x + m_x, y + m_y
        if isinstance(self.surface, pygame.Rect):
            s_x, s_y = self.surface.size
        else:
            s_x, s_y = self.surface.get_size()
        for ent in entity:
            ent_x, ent_y = ent.coord
            if isinstance(ent.surface, pygame.Rect):
                s_ent_x, s_ent_y = ent.surface.size
            else:
                s_ent_x, s_ent_y = ent.surface.get_size()
            if (
                ent_x <= x + s_x <= ent_x + s_ent_x
                and ent_y <= y + s_y <= ent_y + s_ent_y
                or ent_x <= x <= ent_x + s_ent_x
                and ent_y <= y <= ent_y + s_ent_y
                or ent_x <= x <= ent_x + s_ent_x
                and ent_y <= y + s_y <= ent_y + s_ent_y
                or ent_x <= x + s_x <= ent_x + s_ent_x
                and ent_y <= y <= ent_y + s_ent_y
            ):
                if isinstance(ent, PacGum):
                    self.score += ent.score
                    ent.taken = True
                else:
                    self.moove = 0, 0

    def draw(self, surface: pygame.Surface):
        if isinstance(self.surface, pygame.Rect):
            if self.player == 1:
                pygame.draw.rect(surface, "white", self.surface)
            else:
                pygame.draw.rect(surface, "red", self.surface)
            print("ici")
        else:
            surface.blit(self.surface, self.coord)
        w_x, w_y = pygame.display.get_window_size()
        if self.player == 1:
            width = 25
        else:
            width = 75
        surface.blit(
            self.font.render(str(self.score), False, "white"),
            (w_x / (100 / width), 150),
        )
