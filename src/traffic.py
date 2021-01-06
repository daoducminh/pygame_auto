# -*- coding: utf-8 -*-

class Corner:
    def __init__(self, neighbor, corners):
        self.neighbor = neighbor
        self.corners = corners


class Edge:
    def __init__(self, vertices, body, blocked, segments, box):
        self.vertices = vertices
        self.body = body
        self.blocked = blocked
        self.segments = segments
        self.box = box


class Vertex:
    def __init__(
            self, center, corners, body,
            blocked, edges, segments, box
    ):
        self.center = center
        self.corners = corners
        self.body = body
        self.blocked = blocked
        self.edges = edges
        self.segments = segments
        self.box = box


class Board:
    def __init__(self, vertices, edges, map_board):
        self.vertices = vertices
        self.edges = edges
        self.map_board = map_board

    def get_location(self, pos):
        for k, v in self.vertices.items():
            if v.box.contains_point(pos):
                return v
        for e in self.edges:
            if e.box.contains_point(pos):
                return e
        return None
