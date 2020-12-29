# -*- coding: utf-8 -*-

import pygame as p

from constants.styles import *


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
