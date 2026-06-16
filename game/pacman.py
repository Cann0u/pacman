import pygame
from entity import Entity

class Pacman(Entity):
    def __init__(self, pos, player: int):
        super().__init__(pos)
        self.player = player
