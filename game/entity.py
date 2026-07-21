from typing import Tuple, List
import pygame
import math

class Entity:
    def __init__(
        self, pos: Tuple, moove: Tuple, coord: Tuple, sprite: pygame.Surface, hitbox
    ):
        self.pos = pos
        self.coord = coord
        self.surface = sprite
        self.moove = moove
        self.hitbox = hitbox

    def check_collapse(self, entity: List):
        x, y = self.coord
        m_x, m_y = self.moove
        h_x, h_y = self.hitbox
        x, y = x + h_x / 2 + m_x, y + h_y / 2 + m_y 
        for ent in entity:
            e_x, e_y = ent.coord
            he_x, he_y = ent.hitbox
            e_x, e_y = e_x + he_x / 2, e_y + he_y / 2
            if x <= e_x:
                if y <= e_y:
                    if x + h_x / 2 >= e_x - he_x / 2 and y + h_y / 2 >= e_y - he_y / 2:
                        return ent
                if y >= e_y:
                    if x + h_x / 2 >= e_x - he_x / 2 and y - h_y / 2 <= e_y + he_y / 2:
                        return ent
            if x >= e_x:
                if y <= e_y:
                    if x - h_x / 2 <= e_x + he_x / 2 and y + h_y / 2 >= e_y - he_y / 2:
                        return ent
                if y >= e_y:
                    if x - h_x / 2 <= e_x + he_x / 2 and y - h_y / 2 <= e_y + he_y / 2:
                        return ent
                        

    def moove_on(self):
        p_x, p_y = self.coord
        d_x, d_y = self.moove
        w_x, w_y = pygame.display.get_window_size()
        if p_x + d_x < 0:
            self.coord = 0, d_y + p_y
        elif p_y + d_y < 0:
            self.coord = d_x + p_x, 0
        else:
            self.coord = d_x + p_x, d_y + p_y
        if isinstance(self.surface, pygame.Rect):
            self.surface.left, self.surface.top = self.coord

    def draw(self, surface):
        ...

    def event(self, event):
        ...
