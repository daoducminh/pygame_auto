# -*- coding: utf-8 -*-

import pygame as p
from networkx import Graph

from constants.board import *
from constants.car import *
from constants.files import DATA_FILE, BOARD_FILE, GRAPH_FILE
from constants.styles import *
from src.drawer import draw_map, get_vertex_group, draw_blocked_road
from src.helper import read_data, find_shortest_path
from src.sprites import CarSprite
from src.traffic import Board

FPS = 30
fps_clock = p.time.Clock()
CAR_IMAGE = p.image.load(CAR_IMAGE_PATH)

class Game:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.data = read_data(DATA_FILE)
        self.board: Board = read_data(BOARD_FILE)
        self.graph: Graph = read_data(GRAPH_FILE)
        self.vertex_group: p.sprite.Group = get_vertex_group(self.board)
        self.car = CarSprite(
            CAR_INIT_POS,
            CAR_DIRECTION,
            CAR_SIZE,
            0,
            0,
            0,
            CAR_IMAGE
        )
        self.car_group = p.sprite.Group(self.car)
        self.moves = []
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
            if event.type == p.KEYDOWN:
                if event.key == p.K_UP:
                    self.car.speed = CAR_SPEED
                elif event.key == p.K_DOWN:
                    self.car.speed = -CAR_SPEED
                elif event.key == p.K_LEFT:
                    self.car.angle_speed = -CAR_ANGLE_SPEED
                elif event.key == p.K_RIGHT:
                    self.car.angle_speed = CAR_ANGLE_SPEED
            elif event.type == p.KEYUP:
                if event.key == p.K_LEFT:
                    self.car.angle_speed = 0
                elif event.key == p.K_RIGHT:
                    self.car.angle_speed = 0
                elif event.key == p.K_UP:
                    self.car.speed = 0
                elif event.key == p.K_DOWN:
                    self.car.speed = 0
        #     if event.type == p.MOUSEBUTTONDOWN:
        #         a = p.mouse.get_pos()
        #         b = g.board.get_location(*a)
        #         print(b)
        #         if len(self.moves) < 2:
        #             self.vertex_group.update(event_list, self.moves)
        #             if len(self.moves) == 2:
        #                 print(self.moves)
        #                 for s in self.vertex_group.sprites():
        #                     if not s.clicked:
        #                         s.hide()

    def draw(self):
        # self.screen.blit(self.map_surface, MAP_POSITION)
        draw_map(self.screen, self.board.map_board, COLOR_WHITE, 1)
        # draw_vertices(self.screen, self.board, VERTEX_RADIUS)
        # draw_blocked_road(self.screen, (0, 1, 7, 8, 4, 5), self.board, COLOR_RED)
        self.car_group.update()
        self.car_group.draw(self.screen)

        # if len(self.moves) == 2:
        #     path = find_shortest_path(self.graph, *self.moves)
        #     draw_blocked_road(self.screen, path, self.board, COLOR_RED)
        #
        # self.vertex_group.draw(self.screen)


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

        g.handle_events(events)
        g.clear_screen()
        g.draw()

        p.display.flip()
        fps_clock.tick(FPS)
