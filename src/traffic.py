# -*- coding: utf-8 -*-

from math import sin, cos, floor


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


class Vertex:
    def __init__(self, center, corners, body, blocked, edges):
        self.center = center
        self.corners = corners
        self.body = body
        self.blocked = blocked
        self.edges = edges


class Board:
    def __init__(self, vertices, map_board):
        self.vertices = vertices
        # self.edges = edges
        self.map_board = map_board
