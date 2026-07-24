import pygame
from .entity import Entity
from .pacgum import PacGum
from .map import Map
from .pacman import Pacman
import mazegen
import random
from .ghosts import Ghost
from .algo import Algo


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
                    continue

            entity = self.entity.copy()
            entity.pop(i)

            if isinstance(ent, Pacman):
                ent.check_entity(entity)
                e_x, e_y = ent.coord
                s_x, s_y = self.map.start
                ent.pos = int((e_x - s_x) // 20), int((e_y - s_y) // 20)
                ent.check_next(entity)

            elif isinstance(ent, Ghost):
                e_x, e_y = ent.coord
                s_x, s_y = self.map.start
                ent.pos = int((e_x - s_x) // 20), int((e_y - s_y) // 20)

                aligned = (e_x - s_x - 2) % 20 == 0 and (e_y - s_y - 2) % 20 == 0
                if aligned:
                    pacman_ent = next((e for e in entity if isinstance(e, Pacman)), None)
                    if pacman_ent:
                        p_dx, p_dy = pacman_ent.moove
                        pacman_dir = (p_dx // 2 if p_dx else 0, p_dy // 2 if p_dy else 0)
                        ghosts = [e for e in self.entity if isinstance(e, Ghost)]
                        ent.update_target(pacman_ent.pos, pacman_dir, ghosts)

                from .map import Wall
                if isinstance(ent.check_collapse(entity), Wall):
                    continue

            ent.moove_on()

        if pacgum == 0:
            pacman = []
            while self.entity != []:
                ent = self.entity.pop()
                if isinstance(ent, Pacman):
                    pacman.append(ent)
            self.entity += pacman
            self.generate_level(pacman)

    def generate_level(self, pacman: list[Pacman] = None, ghosts: list[Ghost] = None):
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

        if not ghosts:
            nb_ghosts = 4
            for i in range(1, nb_ghosts + 1):
                ghost_spawn = valid.pop(random.randint(0, len(valid) - 1))
                g_x, g_y = ghost_spawn
                c_x, c_y = self.map.start
                self.add_entity(
                    Ghost(
                        ghost_spawn,
                        (g_x * 20 + c_x + 2, g_y * 20 + c_y + 2),
                        None,
                        i,
                        Algo(self.map),
                    )
                )
        else:
            for ghost in ghosts:
                ghost_spawn = valid.pop(random.randint(0, len(valid) - 1))
                g_x, g_y = ghost_spawn
                c_x, c_y = self.map.start
                ghost.pos = ghost_spawn
                ghost.coord = g_x * 20 + c_x + 2, g_y * 20 + c_y + 2
                ghost.algo = Algo(self.map)
                self.add_entity(ghost)

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
