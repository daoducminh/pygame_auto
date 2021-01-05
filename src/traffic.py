# -*- coding: utf-8 -*-

from math import sin, cos, floor

import matplotlib.path as plt_path
import numpy as np
from sympy import Line, Point

from constants.names import BODY


def contain_point(body, point):
    box = plt_path.Path(np.array(body))
    return box.contains_point(point)


class Car:
    def __init__(self, x, y, velocity, turn_rate, angle):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.velocity = velocity
        self.turn_rate = turn_rate
        self.angle = angle

    def go_forward(self):
        self.x += floor(self.velocity * cos(self.angle))
        self.y += floor(self.velocity * sin(self.angle))

    def turn_right(self):
        self.angle += self.turn_rate

    def turn_left(self):
        self.angle -= self.turn_rate


class Corner:
    def __init__(self, neighbor, corners):
        self.neighbor = neighbor
        self.corners = corners


class Edge:
    def __init__(self, vertices, body, blocked):
        self.vertices = vertices
        self.body = body
        self.blocked = blocked
        self.lines = [Line(Point(*i[0]), Point(*i[1])) for i in self.blocked]


class Vertex:
    def __init__(self, center, corners, body, blocked, edges):
        self.center = center
        self.corners = corners
        self.body = body
        self.blocked = blocked
        self.edges = edges
        self.lines = [Line(Point(*i[0]), Point(*i[1]))
                      for i in self.blocked] if self.blocked else None


class Board:
    def __init__(self, vertices, edges, map_board):
        self.vertices = vertices
        self.edges = edges
        self.map_board = map_board

    def get_location(self, x, y):
        # p = Point(x, y)
        for k, v in self.vertices.items():
            if contain_point(v.body, (x, y)):
                return k, v
        for e in self.edges:
            if contain_point(e[BODY], (x, y)):
                return e
        return None
