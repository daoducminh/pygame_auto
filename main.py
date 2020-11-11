# -*- coding: utf-8 -*-

from map import draw_map

class Game:
    def __init__(self):
        pass

    def start(self):
        pass

    def handle_events(self):
        pass

    def draw(self):
        pass


if __name__ == "__main__":
    g = Game()
    g.start()

    while True:
        g.handle_events()
        g.draw()
