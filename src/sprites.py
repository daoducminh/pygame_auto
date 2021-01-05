# -*- coding: utf-8 -*-
from math import degrees

import pygame as p

from constants.styles import *


class CarSprite(p.sprite.Sprite):
    def __init__(
            self, position, direction, car_size,
            speed, angle, angle_speed, car_image
    ):
        super(CarSprite, self).__init__()
        self.original_image = p.Surface(car_size)
        car = p.transform.rotate(
            p.transform.scale(car_image, car_size),
            180 - degrees(angle)
        )
        self.original_image.blit(car, p.Rect((0, 0), car_size))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=position)
        self.position = p.Vector2(position)
        self.direction = p.Vector2(direction)
        self.speed = speed
        self.angle = angle
        self.angle_speed = angle_speed

    def update(self):
        # Rotate the direction vector and then the image.
        self.direction.rotate_ip_rad(self.angle_speed)
        self.angle += self.angle_speed
        self.image = p.transform.rotate(self.original_image, -degrees(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        # Update the position vector and the rect.
        self.position += self.direction * self.speed
        self.rect.center = self.position


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
                    print(f'Click {self.index}')
        self.image = self.clicked_image if self.clicked else self.original_image
