import pygame
from .entity import Entity


class Game:
    def __init__(self, player, activate: bool, surface: pygame.Surface, font):
        self.player = player
        self.state = activate
        self.button = []
        self.focus = 0
        self.font = font
        self.surface = surface
        self.entity = []

    def add_entity(self, entity: Entity | list):
        if isinstance(entity, list):
            self.entity += entity
        else:
            self.entity.append(entity)

    def event(self, event):
        for ent in self.entity:
            ent.event(event)

    def loop(self):
        for ent in self.entity:
            ent.moove_on()

    def draw(self):
        print(self.entity)
        for ent in self.entity:
            ent.draw(self.surface)
