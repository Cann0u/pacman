import pygame
from .entity import Entity
from .pacgum import PacGum
from .map import Map
from .pacman import Pacman
import mazegen


class Game:
    def __init__(
        self,
        player,
        activate: bool,
        surface: pygame.Surface,
        font,
        info,
    ):
        self.player = player
        self.state = activate
        self.button = []
        self.focus = 0
        self.font = font
        self.surface = surface
        self.entity = []
        self.maze = mazegen.MazeGenerator(
            mazegen.MazeConfig(
                height=info["level"]["height"],
                width=info["level"]["width"],
                entry_coord=(0, 0),
                exit_coord=(1, 0),
                output_file="output.txt"
            )
        )
        self.map = Map(self.maze.generate())
        self.map.create()
        self.add_entity(self.map.entity)

    def add_entity(self, entity: Entity | list):
        if isinstance(entity, list):
            self.entity += entity
        else:
            self.entity.append(entity)

    def event(self, event):
        for ent in self.entity:
            ent.event(event)

    def loop(self):
        for i, ent in enumerate(self.entity):
            if isinstance(ent, PacGum):
                if ent.taken:
                    self.entity.pop(i)
                    continue
            entity = self.entity.copy()
            entity.pop(i)
            if isinstance(ent, Pacman):
                ent.check_entity(entity)
            ent.moove_on()

    def draw(self):
        for ent in self.entity:
            ent.draw(self.surface)
