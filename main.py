# -*- coding: utf-8 -*-

import pygame as p
from networkx import Graph

from constants.board import *
from constants.coordinates import CAR_INIT_X, CAR_INIT_Y
from constants.styles import *
from drawer import draw_map, get_vertex_group, draw_blocked_road
from helper import init_board, init_graph, find_shortest_path, init_data
from traffic import Car, Board
from constants.files import PICKLE_FILE

FPS = 30
fps_clock = p.time.Clock()


class Game:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.data = init_data(PICKLE_FILE)
        self.board: Board = init_board(self.data)
        self.graph: Graph = init_graph(self.board)
        self.vertex_group: p.sprite.Group = get_vertex_group(self.board)
        self.moves = []
        self.car = Car(
            CAR_INIT_X,
            CAR_INIT_Y,
            CAR_VELOCITY,
            CAR_TURN_RATE,
            CAR_ANGLE
        )
        icon = p.image.load(ICON_PATH)
        p.display.set_icon(icon)
        p.display.set_caption(PROGRAM_TITLE)

    def clear_screen(self):
        self.screen.fill(0)

    def reset_state(self):
        self.moves.clear()
        for s in self.vertex_group.sprites():
            s.reset()

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == p.MOUSEBUTTONDOWN:
                if len(self.moves) < 2:
                    self.vertex_group.update(event_list, self.moves)
                    if len(self.moves) == 2:
                        print(self.moves)
                        for s in self.vertex_group.sprites():
                            if not s.clicked:
                                s.hide()

        # keys = p.key.get_pressed()
        # if keys[p.K_UP]:
        #     self.car.go_forward()
        # elif keys[p.K_RIGHT]:
        #     self.car.turn_right()
        # elif keys[p.K_LEFT]:
        #     self.car.turn_left()

    def draw(self):
        # self.screen.blit(self.map_surface, MAP_POSITION)
        draw_map(self.screen, COLOR_WHITE, 1)
        # draw_vertices(self.screen, self.board, VERTEX_RADIUS)
        # draw_blocked_road(self.screen, (0, 1, 7, 8, 4, 5), self.board, COLOR_RED)
        # draw_car(self.screen, self.car)

        # if len(self.moves) == 2:
        #     path = find_shortest_path(self.graph, *self.moves)
        #     draw_blocked_road(self.screen, path, self.board, COLOR_RED)

        self.vertex_group.draw(self.screen)


if __name__ == "__main__":
    g = Game()
    while g.running:
        events = p.event.get()
        for e in events:
            if e.type == p.QUIT:
                g.running = False
        keys = p.key.get_pressed()
        if keys[p.K_c]:
            g.reset_state()

        g.clear_screen()
        g.draw()
        g.handle_events(events)

        p.display.flip()
        fps_clock.tick(FPS)
