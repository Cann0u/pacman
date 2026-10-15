from abc import abstractmethod, ABC
from typing import Tuple, List, Any
import pygame


class Entity(ABC):
    pos: Tuple[int, int]
    coord: Tuple[float, float]
    moove: Tuple[int, int]
    hitbox: Tuple[int, int]
    surface: pygame.Surface | pygame.Rect

    def __init__(
        self,
        pos: Tuple[int, int],
        moove: Tuple[int, int],
        coord: Tuple[float, float],
        sprite: pygame.Surface | None = None,
        hitbox: Tuple[int, int] = (0, 0),
    ):
        self.pos: Tuple[int, int] = pos
        self.coord: Tuple[float, float] = coord
        self.moove: Tuple[int, int] = moove
        self.hitbox: Tuple[int, int] = hitbox
        if not sprite:
            self.surface = pygame.Rect(self.coord, self.hitbox)
        else:
            self.surface = sprite

    def check_collapse(self, entity: List["Entity"]) -> Any | None:
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
                    if (
                        x + h_x / 2 >= e_x - he_x / 2
                        and y + h_y / 2 >= e_y - he_y / 2
                    ):
                        return ent
                if y >= e_y:
                    if (
                        x + h_x / 2 >= e_x - he_x / 2
                        and y - h_y / 2 <= e_y + he_y / 2
                    ):
                        return ent
            if x >= e_x:
                if y <= e_y:
                    if (
                        x - h_x / 2 <= e_x + he_x / 2
                        and y + h_y / 2 >= e_y - he_y / 2
                    ):
                        return ent
                if y >= e_y:
                    if (
                        x - h_x / 2 <= e_x + he_x / 2
                        and y - h_y / 2 <= e_y + he_y / 2
                    ):
                        return ent
        return None

    def moove_on(self) -> None:
        p_x, p_y = self.coord
        d_x, d_y = self.moove
        if p_x + d_x < 0:
            self.coord = 0, d_y + p_y
        elif p_y + d_y < 0:
            self.coord = d_x + p_x, 0
        else:
            self.coord = d_x + p_x, d_y + p_y
        if isinstance(self.surface, pygame.Rect):
            self.surface.left, self.surface.top = self.coord

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...

    @abstractmethod
    def event(self, event: pygame.event.Event) -> None: ...
