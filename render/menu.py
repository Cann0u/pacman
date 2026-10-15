import pygame
from typing import Tuple, Callable, List


class Image:
    def __init__(
        self, image: pygame.Surface, coord: Tuple[float, float], size: float
    ):
        self.image_raw = image
        self.coord = coord
        self.w, self.h = self.image_raw.get_size()
        self.size = size
        self.image = pygame.transform.scale(
            self.image_raw, (self.w * size, self.h * size)
        )
        self.w, self.h = self.image.get_size()

    def draw(self, surface: pygame.Surface) -> None:
        w_x, w_y = pygame.display.get_window_size()
        x, y = self.coord
        surface.blit(
            self.image,
            (
                w_x / 2 + x - self.w / 2,
                w_y / 4 + y - self.h / 2,
            ),
        )


class Text:
    def __init__(self, text: str, height: int, width: int):
        self.text = text
        self.width = width
        self.height = height
        self.focus = False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        w_x, w_y = pygame.display.get_window_size()
        length, height = font.size(self.text)
        if self.focus:
            f_length, f_height = font.size("> ")
            surface.blit(
                font.render("> " + self.text, False, "white"),
                (
                    w_x / (100 / self.width) - length / 2 - f_length,
                    w_y / (100 / self.height) - height / 2,
                ),
            )
        else:
            surface.blit(
                font.render(self.text, False, "white"),
                (
                    w_x / (100 / self.width) - length / 2,
                    w_y / (100 / self.height) - height / 2,
                ),
            )


class Button:
    def __init__(
        self, text: str, height: int, width: int, func: Callable[[], None]
    ):
        self.text = text
        self.width = width
        self.height = height
        self.func = func
        self.focus = False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        w_x, w_y = pygame.display.get_window_size()
        length, height = font.size(self.text)
        if self.focus:
            f_length, f_height = font.size("> ")
            surface.blit(
                font.render("> " + self.text, False, "white"),
                (
                    w_x / (100 / self.width) - length / 2 - f_length,
                    w_y / (100 / self.height) - height / 2,
                ),
            )
        else:
            surface.blit(
                font.render(self.text, False, "white"),
                (
                    w_x / (100 / self.width) - length / 2,
                    w_y / (100 / self.height) - height / 2,
                ),
            )


class Menu:
    def __init__(
        self, activate: bool, surface: pygame.Surface, font: pygame.font.Font
    ):
        self.state = activate
        self.images: List[Image] = []
        self.button: List[Button] = []
        self.focus = 0
        self.font = font
        self.end = False
        self.surface = surface
        self.text: List[Text] = []

    def loop(self) -> None:
        pass

    def add_button(self, button: Button) -> None:
        self.button.append(button)

    def add_image(self, image: Image) -> None:
        self.images.append(image)

    def add_text(self, text: Text) -> None:
        self.text.append(text)

    def event(self, event: pygame.event.Event) -> None:
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

    def draw(self) -> None:
        for img in self.images:
            img.draw(self.surface)
        for button in self.button:
            button.draw(self.surface, self.font)
        for text in self.text:
            text.draw(self.surface, self.font)
