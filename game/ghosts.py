from typing import Tuple
import pygame
from .entity import Entity
from .algo import Algo

class Ghost(Entity):
    def __init__(self, pos, coord, sprite, ghost: int, algo: Algo):
        super().__init__(pos, moove, coord, sprite)
        self.ghost = ghost
        self.algo = algo
