import pygame
from game.game import Game, End
import json
from .parser import Parser


class Image:
    def __init__(self, image, coord, size):
        self.image_raw = image
        self.coord = coord
        self.w, self.h = self.image_raw.get_size()
        self.size = size
        self.image = pygame.transform.scale(
            self.image_raw, (self.w * size, self.h * (size))
        )
        self.w, self.h = self.image.get_size()

    def draw(self, surface):
        w_x, w_y = pygame.display.get_window_size()
        x, y = self.coord
        surface.blit(
            self.image,
            (
                w_x / 2 + x - self.w / 2,
                w_y / 3 + y - self.h / 2,
            ),
        )


class Button:
    def __init__(self, text: str, height: int, width: int, func: callable):
        self.text = text
        self.width = width
        self.height = height
        self.func = func
        self.focus = False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        w_x, w_y = pygame.display.get_window_size()
        lenght, height = font.size(self.text)
        if self.focus:
            f_lenght, f_height = font.size("> ")
            surface.blit(
                font.render("> " + self.text, False, "white"),
                (
                    w_x / (100 / self.width) - lenght / 2 - f_lenght,
                    w_y / (100 / self.height) - height / 2,
                ),
            )
        else:
            surface.blit(
                font.render(self.text, False, "white"),
                (
                    w_x / (100 / self.width) - lenght / 2,
                    w_y / (100 / self.height) - height / 2,
                ),
            )


class Menu:
    def __init__(self, activate: bool, surface, font, file):
        self.state = activate
        self.images = []
        self.button = []
        self.focus = 0
        self.font = font
        self.end = False
        self.surface = surface
        with open(file) as file:
            self.score = json.load(file)

    def loop(self):
        pass

    def event(self, event):
        self.button[self.focus].focus = True
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_DOWN:
                    self.button[self.focus].focus = False
                    self.focus = (self.focus + 1) % len(self.button)
                    self.button[self.focus].focus = True
                case pygame.K_UP:
                    self.button[self.focus].focus = False
                    if self.focus == 0:
                        self.focus = len(self.button) - 1
                    else:
                        self.focus = self.focus - 1
                        self.button[self.focus].focus = True
                case pygame.K_SPACE:
                    self.button[self.focus].func()

    def draw(self):
        w_x, w_y = pygame.display.get_window_size()
        for img in self.images:
            img.draw(self.surface)
        for button in self.button:
            button.draw(self.surface, self.font)


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
        self.state.button.append(
            Button(
                "HIGHSCORE :",
                13,
                50,
                self.skip,
            )
        )
        with open(self.parser.info["highscore_filename"]) as file:
            dict = json.load(file)
            for i, user in enumerate(dict["hi_score"]):
                self.state.button.append(
                    Button(
                        f"{user} : {dict['hi_score'][user]}",
                        20 + 7 * i,
                        50,
                        self.skip,
                    )
                )

        self.state.button.append(Button("BACK", 90, 50, self.start))

    def start(self):
        self.state = Menu(
            True,
            self.surface,
            self.font,
            self.parser.info["highscore_filename"],
        )
        self.state.button.append(Button("1 PLAYER", 55, 50, self.launch1))
        self.state.button.append(Button("2 PLAYERS", 65, 50, self.launch2))
        self.state.button.append(Button("HIGHSCORE", 75, 50, self.highscore))
        self.state.button.append(Button("EXIT", 85, 50, self.quit))
        self.state.images.append(
            Image(pygame.image.load("sprite/canvas.png"), (0, 0), 0.75)
        )

    def on_loop(self):
        self.state.loop()
        if self.state.end:
            if isinstance(self.state, Game):
                self.state = End(self.state)
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
