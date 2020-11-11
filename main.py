# -*- coding: utf-8 -*-

import pygame as p

from constants.board import *
from constants.styles import *
from constants.coordinates import MAP_POSITION
from drawer import draw_map


class Game:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.map_surface = p.Surface((MAP_WIDTH, MAP_HEIGHT))

    def start(self):
        icon = p.image.load(ICON_PATH)
        p.display.set_icon(icon)
        p.display.set_caption(PROGRAM_TITLE)

    def handle_events(self):
        for e in p.event.get():
            if e.type == p.QUIT:
                self.running = False

    def draw(self):
        self.screen.blit(self.map_surface, MAP_POSITION)
        draw_map(self.map_surface, COLOR_WHITE, 1)
        p.display.update()


if __name__ == "__main__":
    g = Game()
    g.start()

    while g.running:
        g.handle_events()
        g.draw()
