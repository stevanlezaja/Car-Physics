import pygame as pg

from src.const import *
from src.game import Game

class UI:
    def __init__(self):
        self.game = Game()
        self.speed = 0
        self.rev = 0
        self.gear = 0

    def update(self):
        self.speed = self.game.get_car().get_speed()
        self.rev = self.game.get_car().get_rev()

    def draw(self):
        pass