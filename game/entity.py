import pygame


class Entity:
    def __init__(self, pos: tuple):
        self.pos = pos
        self.move = [0, 0]

    def check_collapse(self):
        ...
