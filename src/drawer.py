# -*- coding: utf-8 -*-

import pygame as p

from constants.board import TRAFFIC_LIGHT_EXCLUDE
from constants.styles import COLOR_RED, COLOR_GREEN
from .sprites import TrafficLightSprite, VertexSprite


def draw_map(surface, map_board, color, width):
    for path in map_board:
        p.draw.lines(
            surface,
            color,
            False,
            path,
            width
        )


# def draw_car(surface, car):
#     car_sprite = p.transform.rotate(
#         p.transform.scale(
#             CAR_IMAGE,
#             (CAR_WIDTH, CAR_HEIGHT)
#         ),
#         180 - degrees(car.angle)
#     )
#     surface.blit(
#         car_sprite,
#         p.Rect(
#             (car.x, car.y),
#             (CAR_WIDTH, CAR_HEIGHT)
#         )
#     )


def draw_blocked_road(surface, path, board, color):
    # Length of path (array of vertices)
    length = len(path)
    # Handle vertices from 1 to n-1
    for i in range(1, length - 1):
        v = board.vertices[path[i]]
        for c in v.corners:
            if c.neighbor != path[i - 1] and c.neighbor != path[i + 1]:
                p.draw.line(
                    surface,
                    color,
                    c.corners[0],
                    c.corners[1]
                )
                v.add_segment(c.corners)
    # Handle vertex 0
    v = board.vertices[path[0]]
    for c in v.corners:
        if c.neighbor != path[1]:
            p.draw.line(
                surface,
                color,
                c.corners[0],
                c.corners[1]
            )
            v.add_segment(c.corners)
    # Handle vertex n
    v = board.vertices[path[length - 1]]
    for c in v.corners:
        if c.neighbor != path[length - 2]:
            p.draw.line(
                surface,
                color,
                c.corners[0],
                c.corners[1]
            )
            v.add_segment(c.corners)


def draw_vertices(surface, board, radius):
    for v in list(board.vertices.values()):
        p.draw.circle(
            surface,
            COLOR_GREEN if v.is_picked else COLOR_RED,
            v.center,
            radius
        )


def get_vertex_group(board):
    sprite_list = []
    for key, value in board.vertices.items():
        sprite_list.append(VertexSprite(key, *value.center))
    return p.sprite.Group(sprite_list)


def get_traffic_light_group(board):
    sprite_list = []
    for key, value in board.vertices.items():
        if key not in TRAFFIC_LIGHT_EXCLUDE:
            sprite_list.append(TrafficLightSprite(key, *value.center))
    return p.sprite.Group(sprite_list)
