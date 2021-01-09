# -*- coding: utf-8 -*-

import pygame as p
from networkx import Graph

from constants.board import *
from constants.car import *
from constants.files import DATA_FILE, BOARD_FILE, GRAPH_FILE, STEERING_FILE, SPEED_FILE
from constants.styles import *
from fuzziness.fuzzification import get_deviation_rules, get_light_rules, get_distance_rules
from fuzziness.inference.speed import SpeedDeduction
from fuzziness.inference.steering import SteeringDeduction
from src.drawer import draw_map, get_traffic_light_group, draw_blocked_road, get_vertex_group
from src.helper import read_data, handle_angle, find_shortest_path
from src.sprites import CarSprite, PERIOD_TIME
from src.traffic import Board, Vertex, Edge

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
        self.car: CarSprite = None
        self.car_group = None
        self.vertex_group: p.sprite.Group = get_vertex_group(self.board)
        self.moves = []
        icon = p.image.load(ICON_PATH)
        p.display.set_icon(icon)
        p.display.set_caption(PROGRAM_TITLE)

        self.steering = SteeringDeduction(STEERING_FILE)
        self.speed = SpeedDeduction(SPEED_FILE)
        self.path = None
        self.current_vertex = None
        self.current_sector = None
        self.next_vertex = None
        self.next_sector = None
        self.cur_path_index = None

        self.traffic_lights = self.traffic_light_group.sprites()
        self.finish = None

    def _(self, angle):
        car_angle = 90 - angle
        if self.cur_path_index < len(self.path) - 1:
            next_p = None
            if isinstance(self.current_sector, Vertex):
                for c in self.current_sector.corners:
                    if c.neighbor == self.next_vertex:
                        next_p = c.midpoint_p
            elif isinstance(self.current_sector, Edge):
                for c in self.board.vertices[self.next_vertex].corners:
                    if c.neighbor == self.current_vertex:
                        next_p = c.midpoint_p
            # i1 = self.path[self.cur_path_index]
            # i2 = self.path[self.cur_path_index + 1]
            # v1 = self.board.vertices[i1]
            # v2 = self.board.vertices[i2]
            # start = v1.center
            start = self.car.pos
            if not next_p:
                v2 = self.board.vertices[self.next_vertex]
                next_p = v2.center
            direction = (next_p[0] - start[0], next_p[1] - start[1])
            dir_vector = p.Vector2(*direction).normalize()
            a = dir_vector.angle_to(self.car.direction)
            if abs(a) >= 180:
                if a > 0:
                    a = a - 360
                else:
                    a = a + 360
            delta = abs(a - car_angle)
            if delta > THRESHOLD:
                return handle_angle(a)
            else:
                return car_angle
        else:
            return car_angle

    def init_car(self, pos):
        start = self.board.vertices[self.path[0]].center
        next_p = self.board.vertices[self.path[1]].center
        direction = (next_p[0] - start[0], next_p[1] - start[1])
        self.car = CarSprite(
            pos,
            direction,
            CAR_SIZE,
            CAR_SPEED,
            CAR_ANGLE_SPEED,
            CAR_IMAGE
        )
        self.car_group = p.sprite.Group(self.car)
        self.current_vertex = self.path[0]
        self.next_vertex = self.path[1]
        self.current_sector = self.board.vertices[self.current_vertex]
        self.next_sector = self.board.vertices[self.next_vertex]
        self.cur_path_index = 0

    def clear_screen(self):
        self.screen.fill(0)

    def reset_state(self):
        self.moves.clear()
        for s in self.traffic_light_group.sprites():
            s.reset()

    def update_current_sector(self):
        current_sector = g.board.get_location(self.car.pos)
        if current_sector and current_sector != self.current_sector:
            self.current_sector = current_sector
            self.next_sector = self.current_sector
            if isinstance(current_sector, Vertex):
                self.cur_path_index += 1
                if self.cur_path_index < len(self.path) - 1:
                    next_v = self.path[self.cur_path_index + 1]
                    if current_sector.index != next_v:
                        self.current_vertex = self.next_vertex
                        self.next_vertex = next_v
                        self.current_sector = current_sector
                        for c in current_sector.corners:
                            if c.neighbor == self.path[self.cur_path_index]:
                                current_sector.add_segment(c.corners)
                                break
                        next_v = self.path[self.cur_path_index + 1]
                        self.next_sector = self.board.vertices[next_v]
                else:
                    self.finish = True

    def handle_car_turn(self):
        if self.current_vertex==11:
            print('')
        l, r = self.car.get_all_distance(self.current_sector, self.next_sector, self.board)
        self.get_distance()
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
        # Convert calculated angle to car angle
        car_angle = self._(a)
        self.car.turn(car_angle)

    def handle_car_speed(self):
        light = self.get_list_status()
        distance = self.get_distance()

        light_rules = get_light_rules(light)
        distance_rules = get_distance_rules(distance)

        speed_total = 0
        weight_total = 0

        for r1 in light_rules:
            for r2 in distance_rules:
                label, args, min_arg = self.speed.deduce(r1, r2)
                speed, weight = self.speed.calculate(label, args, min_arg)
                speed_total += speed * weight
                weight_total += weight
        car_speed = speed_total / weight_total
        self.car.set_speed(car_speed)

    def get_list_status(self):
        for i in self.traffic_lights:
            if i.index == self.next_vertex:
                t = i.time
                if t == -1:
                    return 40
                return t
        return PERIOD_TIME

    def get_distance(self):
        # if isinstance(self.current_sector, Vertex):
        #     # print(self.current_sector.index, self.current_vertex, self.next_vertex)
        #     for c in self.current_sector.corners:
        #         if c.neighbor == self.next_vertex:
        #             return float(c.midpoint_p.distance(self.car.pos_point))
        #
        # elif isinstance(self.current_sector, Edge):
        #     # print(self.current_sector.vertices, self.cur_path_index, self.next_vertex)
        #     v = self.board.vertices[self.next_vertex]
        #     for c in v.corners:
        #         if c.neighbor == self.current_vertex:
        #             return float(self.car.pos_point.distance(c.midpoint_p))

        v = self.board.vertices[self.next_vertex]
        for c in v.corners:
            if c.neighbor == self.current_vertex:
                return float(self.car.pos_point.distance(c.midpoint_p))

    def handle_events(self, event_list):
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

        # if len(self.moves) == 2:
        #     self.path = find_shortest_path(self.graph, *self.moves)
        #     draw_blocked_road(self.screen, self.path, self.board, COLOR_RED)
        #     pos = self.board.vertices[self.path[0]].center
        #     if not self.car:
        #         self.init_car(pos)

        # self.path = [1, 2, 4, 5]
        self.path = find_shortest_path(self.graph, 18, 6)
        draw_blocked_road(self.screen, self.path, self.board, COLOR_RED)
        pos = self.board.vertices[self.path[0]].center
        if not self.car:
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

        # g.handle_events(events)
        g.car_running = True

        g.clear_screen()
        g.draw()
        if g.car_running and not g.finish:
            g.update_current_sector()
            if g.car.speed != 0:
                g.handle_car_turn()
            # g.handle_car_speed()
            g.car_group.update()
            g.car_group.draw(g.screen)

        p.display.flip()
        fps_clock.tick(FPS)
