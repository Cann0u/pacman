import pygame
import json
from game.game_core import Game, End
from .parser import Parser
from .menu import Menu, Button, Image, Text


class Render:
    def __init__(self, file: str):
        pygame.init()
        info = pygame.display.Info()
        self.surface = pygame.display.set_mode(
            (info.current_w, info.current_h)
        )
        pygame.display.set_caption("PACMAN")
        self.parser = Parser(file)
        self.run = True
        self.font = pygame.font.Font("font/ARCADE_N.TTF", 32)
        self.menu = Menu(
            True,
            self.surface,
            self.font
        )
        self.state: Menu | Game | End = self.menu
        self.clock = pygame.time.Clock()

    def on_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.run = False
        self.state.event(event)

    def on_render(self) -> None:
        self.state.draw()
        self.clock.tick(60)

    def launch1(self) -> None:
        self.state = Game(1, True, self.surface, self.font, self.parser.info)

    def launch2(self) -> None:
        self.state = Game(2, True, self.surface, self.font, self.parser.info)

    def skip(self) -> None:
        pass

    def highscore(self) -> None:
        self.state = Menu(
            True,
            self.surface,
            self.font
        )
        self.state.add_text(Text("HIGHSCORE :", 13, 50))
        try:
            with open(self.parser.info.highscore_filename) as file:
                dico = json.load(file)
                for i, user in enumerate(dico["hi_score"]):
                    self.state.add_text(
                        Text(
                            f"{user} : {dico['hi_score'][user]}",
                            20 + 7 * i,
                            50,
                        )
                    )
        except Exception as e:
            print(e)

        self.state.add_button(Button("BACK", 90, 50, self.start))

    def info(self) -> None:
        self.state = Menu(True, self.surface, self.font)
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
            self.state.add_text(Text(text, 20 + 5 * i, 50))
        self.state.add_button(Button("BACK", 90, 50, self.start))

    def start(self) -> None:
        self.state = Menu(
            True,
            self.surface,
            self.font
        )
        self.state.add_button(Button("1 PLAYER", 45, 50, self.launch1))
        self.state.add_button(Button("2 PLAYERS", 55, 50, self.launch2))
        self.state.add_button(Button("INFO", 65, 50, self.info))
        self.state.add_button(Button("HIGHSCORE", 75, 50, self.highscore))
        self.state.add_button(Button("EXIT", 85, 50, self.quit))
        self.state.add_image(
            Image(pygame.image.load("sprite/canvas.png"), (0, 0), 1.5)
        )

    def on_loop(self) -> None:
        self.state.loop()
        if self.state.end:
            if isinstance(self.state, Game):
                prev_state = self.state
                match self.state.end:
                    case "end":
                        self.state = End(prev_state, False)
                    case "win":
                        self.state = End(prev_state, True)
                    case "quit":
                        self.start()
                    case _:
                        return
            if isinstance(self.state, End):
                self.start()
                return

    def on_exec(self) -> None:
        self.start()
        while self.run:
            for event in pygame.event.get():
                self.on_event(event)
            self.surface.fill("black")
            self.on_loop()
            self.on_render()
            pygame.display.update()

    def quit(self) -> None:
        self.run = False
