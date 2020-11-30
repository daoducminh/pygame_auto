# -*- coding: utf-8 -*-

from math import degrees

import pygame as p

from constants.board import CAR_HEIGHT, CAR_WIDTH, CAR_IMAGE_PATH
from constants.coordinates import *
from constants.styles import COLOR_RED, COLOR_GREEN
from sprites import VertexSprite

CAR_IMAGE = p.image.load(CAR_IMAGE_PATH)


def draw_map(surface, color, width):
    p.draw.lines(
        surface,
        color,
        False,
        (
            A1, A2, A3, A4, H2, H1, A1
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            B1, B2, C2, C1, B1
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            B3, B4, C4, C3, B3
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            B5, B6, C6, C5, I4, I3, I2, I1, B5
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            D1, D2, E2, E1, D1
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            D3, D4, E4, E3, D3
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            D5, D6, E6, E5, D5
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            D7, D8, E8, E7, D7
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            F1, F2, J2, J1, J4, J3, G2, G1, K4, K3, K2, K1, F1
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            F3, F4, G4, G3, F3
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            F5, F6, G6, G5, F5
        ),
        width
    )
    p.draw.lines(
        surface,
        color,
        False,
        (
            F7, F8, G8, G7, F7
        ),
        width
    )


def draw_car(surface, car):
    car_sprite = p.transform.rotate(
        p.transform.scale(
            CAR_IMAGE,
            (CAR_WIDTH, CAR_HEIGHT)
        ),
        180 - degrees(car.angle)
    )
    surface.blit(
        car_sprite,
        p.Rect(
            (car.x, car.y),
            (CAR_WIDTH, CAR_HEIGHT)
        )
    )


def draw_blocked_road(surface, path, board, color):
    # Length of path (array of vertices)
    length = len(path)
    # Handle vertices from 1 to n-1
    for i in range(1, length - 1):
        v = board.vertices[path[i]]
        for edge in v.edges:
            if edge.neighbor != path[i - 1] and edge.neighbor != path[i + 1]:
                p.draw.line(
                    surface,
                    color,
                    edge.corners[0],
                    edge.corners[1]
                )
    # Handle vertex 0
    for edge in board.vertices[path[0]].edges:
        if edge.neighbor != path[1]:
            p.draw.line(
                surface,
                color,
                edge.corners[0],
                edge.corners[1]
            )
    # Handle vertex n
    v = board.vertices[path[length - 1]]
    for edge in v.edges:
        if edge.neighbor != path[length - 2]:
            p.draw.line(
                surface,
                color,
                edge.corners[0],
                edge.corners[1]
            )


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
