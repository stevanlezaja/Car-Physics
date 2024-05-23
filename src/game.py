import pygame as pg
from src.car import Car

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1200, 800))
        self.clock = pg.time.Clock()
        self.running = True
        self.car = Car()

    def get_car(self):
        return self.car

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        keys = pg.key.get_pressed()
        self.car.update(keys)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.car.draw(self.screen)
        pg.display.flip()
        self.clock.tick(60)
