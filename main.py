# -*- coding: utf-8 -*-

import pygame as p

from constants.board import *
from constants.coordinates import CAR_INIT_X, CAR_INIT_Y
from constants.styles import *
from drawer import draw_car, draw_map
from models.vehicle import Car

FPS = 30
fps_clock = p.time.Clock()


class Game:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        # self.map_surface = p.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.car = Car(CAR_INIT_X, CAR_INIT_Y, CAR_VELOCITY, CAR_TURN_RATE, CAR_ANGLE)
        icon = p.image.load(ICON_PATH)
        p.display.set_icon(icon)
        p.display.set_caption(PROGRAM_TITLE)

    def start(self):
        pass

    def clear(self):
        self.screen.fill((0, 0, 0))

    def handle_events(self):
        keys = p.key.get_pressed()
        if keys[p.K_UP]:
            self.car.go_forward()
        elif keys[p.K_RIGHT]:
            self.car.turn_right()
        elif keys[p.K_LEFT]:
            self.car.turn_left()
        for e in p.event.get():
            if e.type == p.QUIT:
                self.running = False

    def draw(self):
        # self.screen.blit(self.map_surface, MAP_POSITION)
        draw_map(self.screen, COLOR_WHITE, 1)
        draw_car(self.screen, self.car)
        p.display.update()
        fps_clock.tick(FPS)


if __name__ == "__main__":
    g = Game()
    g.start()
    while g.running:
        g.clear()
        g.handle_events()
        g.draw()
