import pygame
from .entity import Entity
from .pacgum import PacGum
from .map import Map
from .pacman import Pacman
import json
import mazegen
import random
from render.menu import Menu, Button


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
        self.pause = False
        self.font = font
        self.surface = surface
        self.entity = []
        self.info = info
        self.level = 0
        self.generate_level(seed=self.info["seed"])
        self.time = self.info["level_max_time"]
        self.start_time = pygame.time.get_ticks()
        self.end = None
        self.menu = Menu(False, self.surface, self.font, None)
        self.menu.button.append(Button("Resume", 50, 50, self.resume))
        self.menu.button.append(Button("Exit", 60, 50, self.quit))

    def quit(self):
        self.end = "quit"

    def resume(self):
        self.pause = False

    def add_entity(self, entity: Entity | list):
        if isinstance(entity, list):
            self.entity += entity
        else:
            self.entity.append(entity)

    def event(self, event):
        if self.pause:
            self.menu.event(event)
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause = True
        for i, ent in enumerate(self.entity):
            if isinstance(ent, Pacman):
                entity = self.entity.copy()
                entity.pop(i)
                ent.event(event, entity)
            else:
                ent.event(event)

    def loop(self):
        if self.end or self.pause:
            return
        if (pygame.time.get_ticks() - self.start_time) // 1000 > self.time:
            self.end = "end"
            return
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
            self.level += 1
            if self.level == len(self.info["level"]):
                self.end = "win"
                return
            self.generate_level(pacman)
            self.start_time = pygame.time.get_ticks()

    def generate_level(self, pacman: list[Pacman] = None, seed: int = None):
        self.maze = mazegen.MazeGenerator(
            mazegen.MazeConfig(
                height=self.info["level"][self.level]["height"],
                width=self.info["level"][self.level]["width"],
                entry_coord=(0, 0),
                exit_coord=(1, 0),
                output_file="output.txt",
                seed=seed
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
                        0,
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
        if self.pause:
            self.menu.draw()
            return
        w_x, w_y = pygame.display.get_window_size()
        time = self.time - (pygame.time.get_ticks() - self.start_time) // 1000
        f_x, f_y = self.font.size(str(time))
        self.surface.blit(
            self.font.render(str(time), False, "white"),
            (w_x - f_x, w_y - f_y * 4),
        )
        self.surface.blit(
            self.font.render("level: " + str(self.level + 1), False, "white"),
            (0, w_x // 2),
        )
        for ent in self.entity:
            ent.draw(self.surface)


class End:
    def __init__(self, state: Game, win: bool):
        self.score = sum(
            [i.score for i in state.entity if isinstance(i, Pacman)]
        )
        self.win = win
        self.surface = state.surface
        self.font = state.font
        self.end = False
        self.name = ""
        self.letter = 0
        self.player = state.player
        self.hi_score = state.info["highscore_filename"]
        with open(self.hi_score) as file:
            self.d_score = json.load(file)
        self.d_score = dict(
            sorted(self.d_score["hi_score"].items(), key=lambda item: item[1])
        )

    def loop(self): ...

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if (
                    min(self.d_score.values()) < self.score
                    or len(self.d_score.values()) < 10
                ):
                    if self.player == 1:
                        self.d_score[self.name] = self.score
                    else:
                        self.d_score["duo " + self.name] = self.score
                self.d_score = dict(
                    sorted(
                        self.d_score.items(),
                        key=lambda item: item[1],
                        reverse=True,
                    )
                )
                if len(self.d_score) > 10:
                    self.d_score = {
                        j: self.d_score[j]
                        for i, j in enumerate(self.d_score)
                        if i < 10
                    }
                with open(self.hi_score, "w") as file:
                    json.dump({"hi_score": self.d_score}, file, indent=4)
                self.end = True
            if event.key < 255 and len(self.name) < 5:
                self.name += chr(event.key)

    def draw(self):
        w_x, w_y = pygame.display.get_window_size()
        if self.win:
            f_x, f_y = self.font.size("Victory")
            self.surface.blit(
                self.font.render("Victory", False, "green"),
                (w_x / 2 - f_x, w_y / 2 - f_y),
            )
        else:
            f_x, f_y = self.font.size("GAME OVER")
            self.surface.blit(
                self.font.render("GAME OVER", False, "red"),
                (w_x / 2 - f_x, w_y / 2 - f_y),
            )
        f_x, f_y = self.font.size("Name : ")
        self.surface.blit(
            self.font.render("Name :", False, "white"),
            (w_x / 2 - f_x, w_y / 2 + f_y),
        )
        self.surface.blit(
            self.font.render(self.name, False, "white"),
            (w_x / 2, w_y / 2 + f_y),
        )
