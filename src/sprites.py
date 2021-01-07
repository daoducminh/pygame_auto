# -*- coding: utf-8 -*-
from math import radians

import pygame as p
from sympy import Ray, Point

from constants.styles import *

RED_TIME = 90
GREEN_TIME = 90
PERIOD_TIME = RED_TIME + GREEN_TIME


class CarSprite(p.sprite.Sprite):
    def __init__(
            self, position, direction, car_size,
            speed, angle_speed, car_image
    ):
        super(CarSprite, self).__init__()
        self.position = p.Vector2(position)
        self.direction = p.Vector2(direction)
        self.angle = self.direction.angle_to(p.Vector2(1, 0))
        self.speed = speed
        self.angle_speed = angle_speed
        self.original_image = p.Surface(car_size)
        car = p.transform.rotate(
            p.transform.scale(car_image, car_size),
            180 - self.angle
        )
        self.original_image.blit(car, p.Rect((0, 0), car_size))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=position)
        self.left_ray = Ray(position, angle=radians(self.angle - 90))
        self.right_ray = Ray(position, angle=radians(self.angle + 90))
        self.front_ray = Ray(position, angle=radians(self.angle))
        self.pos_point = Point(position)
        self.pos = position

    def update(self):
        self.accelerate(3)
        self.rect.center = self.position

    def update_rays(self):
        self.left_ray = Ray(self.pos_point, angle=radians(self.angle - 90))
        self.right_ray = Ray(self.pos_point, angle=radians(self.angle + 90))
        self.front_ray = Ray(self.pos_point, angle=radians(self.angle))

    def get_all_distance(self, board):
        left, right, front = [], [], []
        for _, v in board.vertices.items():
            for s in v.segments:
                left += self.left_ray.intersection(s)
                right += self.right_ray.intersection(s)
                front += self.front_ray.intersection(s)
        for e in board.edges:
            for s in e.segments:
                left += self.left_ray.intersection(s)
                right += self.right_ray.intersection(s)
                front += self.front_ray.intersection(s)
        left_dist = [self.pos_point.distance(i) for i in left]
        right_dist = [self.pos_point.distance(i) for i in right]
        front_dist = [self.pos_point.distance(i) for i in front]
        return (
            float(min(left_dist)) if left_dist else 1000,
            float(min(right_dist)) if right_dist else 1000,
            float(min(front_dist)) if front_dist else 1000
        )

    def accelerate(self, factor):
        self.position += self.direction * factor * self.speed
        self.pos = (self.position.x, self.position.y)
        self.pos_point = Point(self.pos)
        self.update_rays()
        # print(self.pos)

    def turn(self, factor):
        self.direction.rotate_ip(-factor * self.angle_speed)
        self.angle -= factor * self.angle_speed
        self.image = p.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.update_rays()
        # print(self.angle)


class TrafficLightSprite(p.sprite.Sprite):
    def __init__(self, index, x, y):
        super().__init__()
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
