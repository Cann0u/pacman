import pygame
import json
from game.game import Game, End
from .parser import Parser
from .menu import Menu, Button, Image, Text


class Render:
    def __init__(self, file):
        pygame.init()
        info = pygame.display.Info()
        self.surface = pygame.display.set_mode(
            (info.current_w, info.current_h)
        )
        pygame.display.set_caption("PACMAN")
        pygame.RESIZABLE
        self.parser = Parser(file)
        self.run = True
        self.font = pygame.font.Font("font/ARCADE_N.TTF", 32)
        self.menu = Menu(
            True,
            self.surface,
            self.font,
            self.parser.info["highscore_filename"],
        )
        self.state = self.menu
        self.clock = pygame.time.Clock()

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.run = False
        self.state.event(event)

    def on_render(self):
        self.state.draw()
        self.clock.tick(60)

    def launch1(self):
        self.state = Game(1, True, self.surface, self.font, self.parser.info)
        w_x, w_y = pygame.display.get_window_size()

    def launch2(self):
        self.state = Game(2, True, self.surface, self.font, self.parser.info)
        w_x, w_y = pygame.display.get_window_size()

    def skip(self):
        pass

    def highscore(self):
        self.state = Menu(
            True,
            self.surface,
            self.font,
            self.parser.info["highscore_filename"],
        )
        self.state.text.append(
            Text(
                "HIGHSCORE :",
                13,
                50
            )
        )
        with open(self.parser.info["highscore_filename"]) as file:
            dict = json.load(file)
            for i, user in enumerate(dict["hi_score"]):
                self.state.text.append(
                    Text(
                        f"{user} : {dict['hi_score'][user]}",
                        20 + 7 * i,
                        50
                    )
                )

        self.state.button.append(Button("BACK", 90, 50, self.start))

    def info(self):
        self.state = Menu(True, self.surface, self.font, None)
        texts = [
            "Welcome to pacman.",
            "use wasd to move:",
            "'w' go up",
            "'a' go left",
            "'s' go right",
            "'d' go down",
            "like the real pacman you die if you hit a ghost",
            "or if the time expire.",
            "Your goal was to eat every pacgum in the level,",
            "and finish all the level.",
            "Have fun.",
        ]
        for i, text in enumerate(texts):
            self.state.text.append(Text(text, 20 + 5 * i, 50))
        self.state.button.append(Button("BACK", 90, 50, self.start))

    def start(self):
        self.state = Menu(
            True,
            self.surface,
            self.font,
            self.parser.info["highscore_filename"],
        )
        self.state.button.append(Button("1 PLAYER", 45, 50, self.launch1))
        self.state.button.append(Button("2 PLAYERS", 55, 50, self.launch2))
        self.state.button.append(Button("INFO", 65, 50, self.info))
        self.state.button.append(Button("HIGHSCORE", 75, 50, self.highscore))
        self.state.button.append(Button("EXIT", 85, 50, self.quit))
        self.state.images.append(
            Image(pygame.image.load("sprite/canvas.png"), (0, 0), 1.5)
        )

    def on_loop(self):
        self.state.loop()
        if self.state.end:
            if isinstance(self.state, Game):
                if self.state.end == "end":
                    self.state = End(self.state, False)
                if self.state.end == "win":
                    self.state = End(self.state, True)
                if self.state.end == "quit":
                    self.start()
                return
            if isinstance(self.state, End):
                self.start()
                return

    def on_exec(self):
        self.start()
        while self.run:
            for event in pygame.event.get():
                self.on_event(event)
            self.surface.fill("black")
            self.on_loop()
            self.on_render()
            pygame.display.update()

    def quit(self):
        self.run = False
