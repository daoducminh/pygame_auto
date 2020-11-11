# -*- coding: utf-8 -*-

from pygame.draw import lines

from constants.coordinates import *


def draw_map(surface, color, width):
    lines(
        surface,
        color,
        False,
        (
            A1, A2, A3, A4, H2, H1, A1
        ),
        width
    )
    lines(
        surface,
        color,
        False,
        (
            B1, B2, C2, C1, B1
        ),
        width
    )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         B3, B4, C4, C3, B3
    #     ),
    #     width
    # )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         B5, B6, C6, C5, I4, I3, I2, I1, B5
    #     ),
    #     width
    # )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         D1, D2, E2, E1, D1
    #     ),
    #     width
    # )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         D3, D4, E4, E3, D3
    #     ),
    #     width
    # )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         D5, D6, E6, E5, D5
    #     ),
    #     width
    # )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         D7, D8, E8, E7, D7
    #     ),
    #     width
    # )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         F1, F2, J2, J1, J4, J3, G2, G1, K4, K3, K2, K1, F1
    #     ),
    #     width
    # )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         F3, F4, G4, G3, F3
    #     ),
    #     width
    # )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         F5, F6, G6, G5, F5
    #     ),
    #     width
    # )
    # lines(
    #     surface,
    #     color,
    #     False,
    #     (
    #         F7, F8, G8, G7, F7
    #     ),
    #     width
    # )
