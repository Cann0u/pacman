import pygame
from .entity import Entity
from .pacgum import PacGum
from .map import Map
from .pacman import Pacman
import mazegen
import random


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
        self.info = info
        self.generate_level()

    def add_entity(self, entity: Entity | list):
        if isinstance(entity, list):
            self.entity += entity
        else:
            self.entity.append(entity)

    def event(self, event):
        for i, ent in enumerate(self.entity):
            if isinstance(ent, Pacman):
                entity = self.entity.copy()
                entity.pop(i)
                ent.event(event, entity)
            else:
                ent.event(event)

    def loop(self):
        pacgum = 0
        for i, ent in enumerate(self.entity):
            if isinstance(ent, PacGum):
                pacgum += 1
                if ent.taken:
                    self.entity.pop(i)
            entity = self.entity.copy()
            entity.pop(i)
            if isinstance(ent, Pacman):
                ent.check_entity(entity)
                e_x, e_y = ent.coord
                s_x, s_y = self.map.start
                ent.pos = (e_x - s_x) // 20, (e_y - s_y) // 20
                ent.check_next(entity)
            ent.moove_on()
        if pacgum == 0:
            pacman = []
            while self.entity != []:
                ent = self.entity.pop()
                if isinstance(ent, Pacman):
                    pacman.append(ent)
            self.entity += pacman
            self.generate_level(pacman)

    def generate_level(self, pacman: list[Pacman] = None):
        self.maze = mazegen.MazeGenerator(
            mazegen.MazeConfig(
                height=self.info["level"]["height"],
                width=self.info["level"]["width"],
                entry_coord=(0, 0),
                exit_coord=(1, 0),
                output_file="output.txt",
            )
        )
        self.maze.generate()
        self.map = Map(self.maze.maze)
        self.map.create()
        self.add_entity(self.map.entity)
        if not pacman:
            for i in range(1, self.player + 1):
                self.add_entity(
                    Pacman(
                        (21, 19 + i * 2),
                        (0, 0),
                        self.map.start,
                        None,
                        i,
                        self.font,
                        (16, 16),
                        self.info["lives"],
                        0
                    )
                )
        else:
            for pac in pacman:
                x, y = pac.spawn
                pac.pos = x, y
                c_x, c_y = self.map.start
                pac.coord = x * 20 + c_x + 2, y * 20 + c_y + 2
        valid = self.check_valid()
        if self.info["pacgum"] > len(valid):
            raise ValueError("To many PacGum")
        for i in range(self.info["pacgum"]):
            idc = random.randint(0, len(valid) - 1)
            self.add_entity(
                PacGum(
                    valid[idc],
                    (0, 0),
                    self.map.start,
                    None,
                    self.info["points_per_pacgum"],
                    (8, 8),
                )
            )
            valid.pop(idc)

    def check_valid(self):
        valid = []
        for i, line in enumerate(self.maze.maze):
            for j, col in enumerate(line):
                if col == "*":
                    if (
                        self.maze.maze[i - 1][j] == "*"
                        or self.maze.maze[i + 1][j] == "*"
                        or self.maze.maze[i][j - 1] == "*"
                        or self.maze.maze[i][j + 1] == "*"
                    ):
                        valid.append((j, i))
        return valid

    def draw(self):
        for ent in self.entity:
            ent.draw(self.surface)
