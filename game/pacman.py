import pygame
from .entity import Entity
from .map import Wall
from typing import List


class Pacman(Entity):
    def __init__(
        self,
        pos,
        moove,
        coord,
        sprite,
        player: int,
        font: pygame.font.Font,
        hitbox,
    ):
        super().__init__(pos, moove, coord, sprite, hitbox)
        self.player = player
        self.score = 0
        self.font = font
        x, y = self.pos
        c_x, c_y = self.coord
        self.ent_coord = x * 20 + 2, y * 20 + 2
        if not sprite:
            self.surface = pygame.Rect(self.ent_coord, self.hitbox)
        else:
            self.surface = sprite

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

    def check_entity(self, entity: List[Entity]):
        ent = self.check_collapse(entity)
        from .pacgum import PacGum

        if isinstance(ent, PacGum):
            self.score += ent.score
            ent.taken = True
        if isinstance(ent, Pacman) or isinstance(ent, Wall):
            self.moove = 0, 0

    def draw(self, surface: pygame.Surface):
        if isinstance(self.surface, pygame.Rect):
            if self.player == 1:
                pygame.draw.rect(surface, "yellow", self.surface)
            else:
                pygame.draw.rect(surface, "darkblue", self.surface)
        else:
            surface.blit(self.surface, self.coord)
        w_x, w_y = pygame.display.get_window_size()
        if self.player == 1:
            width = 25
        else:
            width = 75
        surface.blit(
            self.font.render(str(self.score), False, "white"),
            (w_x / (100 / width), 0),
        )
