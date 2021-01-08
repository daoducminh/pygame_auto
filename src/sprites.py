# -*- coding: utf-8 -*-
from math import radians

import pygame as p
from sympy import Ray, Point

from constants.car import MAX_SCAN_DISTANCE
from constants.styles import *
from src.traffic import Vertex, Edge

RED_TIME = 10
GREEN_TIME = 10
PERIOD_TIME = RED_TIME + GREEN_TIME


class CarSprite(p.sprite.Sprite):
    def __init__(
            self, position, direction, car_size,
            speed, angle_speed, car_image
    ):
        super(CarSprite, self).__init__()
        self.position = p.Vector2(position)
        self.direction = p.Vector2(direction).normalize()
        self.angle = self.direction.angle_to(p.Vector2(1, 0))
        self.speed = speed
        self.angle_speed = angle_speed
        self.original_image = p.Surface(car_size)
        car = p.transform.rotate(
            p.transform.scale(car_image, car_size),
            self.angle - 180
        )
        self.original_image.blit(car, p.Rect((0, 0), car_size))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=position)
        self.left_ray = Ray(position, angle=radians(self.angle - 90))
        self.right_ray = Ray(position, angle=radians(self.angle + 90))
        # self.front_ray = Ray(position, angle=radians(self.angle))
        self.pos_point = Point(position)
        self.pos = position

    def update(self):
        self.accelerate(1)
        self.rect.center = self.position

    def update_rays(self):
        self.left_ray = Ray(self.pos_point, angle=radians(self.angle - 90))
        self.right_ray = Ray(self.pos_point, angle=radians(self.angle + 90))

    def get_all_distance(self, sector, next_sector, board):
        left, right = [], []
        if isinstance(sector, Edge):
            self.distance_1(sector.segments, left, right)
            vs = tuple(board.vertices[i] for i in sector.vertices)
            for v in vs:
                self.distance_1(v.segments, left, right)

        elif isinstance(sector, Vertex):
            self.distance_1(sector.segments, left, right)
            if sector != next_sector:
                a, b = sector.index, next_sector.index
                if a < b:
                    vertices = (a, b)
                else:
                    vertices = (b, a)
                for e in sector.edges:
                    if e.vertices == vertices:
                        self.distance_1(e.segments, left, right)
        min_left = float(min(left)) if left else MAX_SCAN_DISTANCE
        min_right = float(min(right)) if right else MAX_SCAN_DISTANCE
        return (
            min_left if min_left else 1,
            min_right if min_right else 1,
        )

    def accelerate(self, factor):
        self.position += self.direction * factor * self.speed
        self.pos = (self.position.x, self.position.y)
        self.pos_point = Point(self.pos)
        self.update_rays()

    def turn(self, factor):
        self.direction.rotate_ip(-factor * self.angle_speed)
        self.angle -= factor * self.angle_speed
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle <= -360:
            self.angle += 360
        self.image = p.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.update_rays()

    def set_speed(self, speed):
        self.speed = speed

    def distance_1(self, segments, left, right):
        """
        For vertex
        """
        for s in segments:
            p1 = self.left_ray.intersection(s)
            p2 = self.right_ray.intersection(s)
            if p1:
                for t in p1:
                    left.append(self.pos_point.distance(t))
            if p2:
                for t in p2:
                    right.append(self.pos_point.distance(t))

    def distance_2(self, segments, left, right):
        """
        For edges
        """
        for s in segments:
            p1 = self.left_ray.intersection(s)
            p2 = self.right_ray.intersection(s)
            if p1:
                left.append(self.pos_point.distance(s))
            if p2:
                right.append(self.pos_point.distance(s))


class TrafficLightSprite(p.sprite.Sprite):
    def __init__(self, index, x, y):
        super(TrafficLightSprite, self).__init__()
        self.index = index
        self.is_green = True
        self.time = PERIOD_TIME
        self.red_light = p.Surface((VERTEX_SIZE, VERTEX_SIZE))
        p.draw.circle(
            self.red_light,
            COLOR_RED,
            (VERTEX_RADIUS, VERTEX_RADIUS),
            VERTEX_RADIUS
        )

        self.green_light = p.Surface((VERTEX_SIZE, VERTEX_SIZE))
        p.draw.circle(
            self.green_light,
            COLOR_GREEN,
            (VERTEX_RADIUS, VERTEX_RADIUS),
            VERTEX_RADIUS
        )

        self.background = p.Surface((VERTEX_SIZE, VERTEX_SIZE))
        p.draw.circle(
            self.background,
            COLOR_BLACK,
            (VERTEX_RADIUS, VERTEX_RADIUS),
            VERTEX_RADIUS
        )

        self.image = self.green_light
        self.rect = self.image.get_rect(center=(x, y))

    def reset(self):
        self.image = self.background

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.time = PERIOD_TIME
            self.is_green = True
        elif self.time == RED_TIME:
            self.is_green = False
        self.image = self.green_light if self.is_green else self.red_light


class VertexSprite(p.sprite.Sprite):
    def __init__(self, index, x, y):
        super().__init__()

        self.clicked = False
        self.index = index

        self.original_image = p.Surface((VERTEX_SIZE, VERTEX_SIZE))
        p.draw.circle(
            self.original_image,
            COLOR_RED,
            (VERTEX_RADIUS, VERTEX_RADIUS),
            VERTEX_RADIUS
        )

        self.clicked_image = p.Surface((VERTEX_SIZE, VERTEX_SIZE))
        p.draw.circle(
            self.clicked_image,
            COLOR_GREEN,
            (VERTEX_RADIUS, VERTEX_RADIUS),
            VERTEX_RADIUS
        )

        self.background = p.Surface((VERTEX_SIZE, VERTEX_SIZE))
        p.draw.circle(
            self.background,
            COLOR_BLACK,
            (VERTEX_RADIUS, VERTEX_RADIUS),
            VERTEX_RADIUS
        )

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

    def hide(self):
        self.image = self.background

    def reset(self):
        self.image = self.original_image
        self.clicked = False

    def update(self, event_list, moves):
        for e in event_list:
            if e.type == p.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(e.pos):
                    self.clicked = not self.clicked
                    moves.append(self.index)
        self.image = self.clicked_image if self.clicked else self.original_image
