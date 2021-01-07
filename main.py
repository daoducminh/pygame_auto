# -*- coding: utf-8 -*-

import pygame as p
from networkx import Graph

from constants.board import *
from constants.car import *
from constants.files import DATA_FILE, BOARD_FILE, GRAPH_FILE, STEERING_FILE, SPEED_FILE
from constants.styles import *
from fuzziness.fuzzification import get_deviation_rules
from fuzziness.inference.speed import SpeedDeduction
from fuzziness.inference.steering import SteeringDeduction
from src.drawer import draw_map, get_traffic_light_group, draw_blocked_road, get_vertex_group
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
        self.car_running = False
        self.data = read_data(DATA_FILE)
        self.board: Board = read_data(BOARD_FILE)
        self.graph: Graph = read_data(GRAPH_FILE)
        self.traffic_light_group: p.sprite.Group = get_traffic_light_group(self.board)
        self.car = None
        self.car_group = None
        self.vertex_group: p.sprite.Group = get_vertex_group(self.board)
        self.moves = []
        icon = p.image.load(ICON_PATH)
        p.display.set_icon(icon)
        p.display.set_caption(PROGRAM_TITLE)

        self.steering = SteeringDeduction(STEERING_FILE)
        self.speed = SpeedDeduction(SPEED_FILE)
        self.path = None

    def init_car(self, pos):
        self.car = CarSprite(
            pos,
            CAR_DIRECTION,
            CAR_SIZE,
            CAR_SPEED,
            CAR_ANGLE_SPEED,
            CAR_IMAGE
        )
        self.car_group = p.sprite.Group(self.car)

    def clear_screen(self):
        self.screen.fill(0)

    def reset_state(self):
        self.moves.clear()
        for s in self.traffic_light_group.sprites():
            s.reset()

    def handle_car_turn(self):
        # pos = g.board.get_location(self.car.pos)
        # if isinstance(pos, Vertex):
        #     print('Vertex')
        # if isinstance(pos, Edge):
        #     print('Edge')
        l, r, f = self.car.get_all_distance(self.board)
        dev = l / (l + r)
        rules = get_deviation_rules(dev)
        angle_total = 0
        weight_total = 0
        for rule in rules:
            label, args, min_arg = self.steering.deduce(rule)
            angle, weight = self.steering.calculate(label, args, min_arg)
            angle_total += angle * weight
            weight_total += weight
        a = angle_total / weight_total
        car_turn = 90 - a + self.car.angle
        self.car.turn(car_turn)

    def handle_car_speed(self):
        pos = g.board.get_location(self.car.pos)

    def handle_events(self, event_list):
        pass
        for event in event_list:
            #     if event.type == p.KEYDOWN:
            #         if event.key == p.K_UP:
            #             self.car.accelerate(2)
            #         elif event.key == p.K_DOWN:
            #             self.car.accelerate(-2)
            #         elif event.key == p.K_LEFT:
            #             self.car.turn(1)
            #         elif event.key == p.K_RIGHT:
            #             self.car.turn(-1)

            if event.type == p.MOUSEBUTTONDOWN:
                if len(self.moves) < 2:
                    self.vertex_group.update(event_list, self.moves)
                    if len(self.moves) == 2:
                        self.car_running = True
                        for s in self.vertex_group.sprites():
                            s.hide()

    def draw(self):
        # self.screen.blit(self.map_surface, MAP_POSITION)
        draw_map(self.screen, self.board.map_board, COLOR_WHITE, 1)
        # draw_vertices(self.screen, self.board, VERTEX_RADIUS)

        # draw_blocked_road(self.screen, (0, 1, 7, 6), self.board, COLOR_RED)

        # if len(self.moves) == 2:
        #     path = find_shortest_path(self.graph, *self.moves)
        #     draw_blocked_road(self.screen, path, self.board, COLOR_RED)
        #

        if len(self.moves) == 2:
            self.path = find_shortest_path(self.graph, *self.moves)
            draw_blocked_road(self.screen, self.path, self.board, COLOR_RED)
            pos = self.board.vertices[self.path[0]].center
            self.init_car(pos)

        self.vertex_group.draw(self.screen)

        if self.car_running:
            self.traffic_light_group.update()
            self.traffic_light_group.draw(self.screen)


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
        if g.car_running:
            g.handle_car_turn()
            g.car_group.update()
            g.car_group.draw(g.screen)

        p.display.flip()
        fps_clock.tick(FPS)
