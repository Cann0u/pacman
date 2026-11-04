from __future__ import annotations
import pygame


class Entity:
    def __init__(
        self,
        pos: tuple[int, int],
        moove: tuple[int, int],
        coord: tuple[float, float],
        hitbox: tuple[int, int] = (0, 0),
        speed: float = 0,
    ) -> None:
        self.pos: tuple[int, int] = pos
        self.coord: tuple[float, float] = coord
        self.moove: tuple[int, int] = moove
        self.hitbox: tuple[int, int] = hitbox
        self.speed: float = speed
        self.accu_move = 0
        self.surface = pygame.Rect(self.coord, self.hitbox)

    def check_collapse(self, entity: list[Entity]) -> Entity | None:
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
        w_x, w_y = pygame.display.get_window_size()
        if p_x + d_x < 0:
            self.coord = 0, d_y + p_y
        elif p_y + d_y < 0:
            self.coord = d_x + p_x, 0
        else:
            self.coord = d_x + p_x, d_y + p_y
        self.surface.left = int(self.coord[0])
        self.surface.top = int(self.coord[1])

    def draw(self, surface: pygame.surface.Surface) -> None: ...

    def event(
        self, event: pygame.event.Event, entity: list[Entity] | None = None
    ) -> None: ...
