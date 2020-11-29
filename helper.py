# -*- coding: utf-8 -*-

from constants.coordinates import *
from traffic import Vertex, Edge, Board


def init_board():
    return Board(
        (
            Vertex(
                0,
                V0,
                (
                    Edge(1, (A2, B1)),
                    Edge(6, (B1, L5))
                )
            ),
            Vertex(
                1,
                V1,
                (
                    Edge(2, (L2, B3)),
                    Edge(7, (B3, B2)),
                    Edge(0, (B2, L1))
                )
            ),
            Vertex(
                2,
                V2,
                (
                    Edge(3, (L4, B5)),
                    Edge(4, (B5, B4)),
                    Edge(1, (B4, L3))
                )
            ),
            Vertex(
                3,
                V3,
                (
                    Edge(10, (L6, B6)),
                    Edge(2, (B6, A3))
                )
            ),
            Vertex(
                4,
                V4,
                (
                    Edge(2, (M1, I1)),
                    Edge(5, (I1, I4)),
                    Edge(8, (I4, M2))
                )
            ),
            Vertex(
                5,
                V5,
                (
                    Edge(4, (I3, I2))
                )
            ),
            Vertex(
                6,
                V6,
                (
                    Edge(0, (L7, C1)),
                    Edge(7, (C1, D1)),
                    Edge(11, (D1, L9))
                )
            ),
            Vertex(
                7,
                V7,
                (
                    Edge(1, (C2, C3)),
                    Edge(8, (C3, D3)),
                    Edge(12, (D3, D2)),
                    Edge(6, (D2, C2))
                )
            ),
            Vertex(
                8,
                V8,
                (
                    Edge(4, (C4, C5)),
                    Edge(9, (C5, D5)),
                    Edge(13, (D5, D4)),
                    Edge(7, (D4, C4))
                )
            ),
            Vertex(
                9,
                V9,
                (
                    Edge(10, (L26, D7)),
                    Edge(14, (D7, D6)),
                    Edge(8, (D6, L25))
                )
            ),
            Vertex(
                10,
                V10,
                (
                    Edge(3, (C6, L8)),
                    Edge(15, (L10, D8)),
                    Edge(9, (D8, C6))
                )
            ),
            Vertex(
                11,
                V11,
                (
                    Edge(6, (L11, E1)),
                    Edge(12, (E1, F1)),
                    Edge(18, (F1, L13))
                )
            ),
            Vertex(
                12,
                V12,
                (
                    Edge(7, (E2, E3)),
                    Edge(13, (E3, F3)),
                    Edge(17, (F3, F2)),
                    Edge(11, (F2, E2))
                )
            ),
            Vertex(
                13,
                V13,
                (
                    Edge(8, (E4, E5)),
                    Edge(14, (E5, F5)),
                    Edge(22, (F5, F4)),
                    Edge(12, (F4, E4))
                )
            ),
            Vertex(
                14,
                V14,
                (
                    Edge(9, (E6, E7)),
                    Edge(15, (E7, F7)),
                    Edge(23, (F7, F6)),
                    Edge(13, (F6, E6))
                )
            ),
            Vertex(
                15,
                V15,
                (
                    Edge(10, (E8, L12)),
                    Edge(24, (L14, F8)),
                    Edge(14, (F8, E8))
                )
            ),
            Vertex(
                16,
                V16,
                (
                    Edge(17, (J1, J4))
                )
            ),
            Vertex(
                17,
                V17,
                (
                    Edge(12, (J2, M3)),
                    Edge(21, (M4, J3)),
                    Edge(16, (J3, J2))
                )
            ),
            Vertex(
                18,
                V18,
                (
                    Edge(11, (M5, K1)),
                    Edge(19, (K1, K4)),
                    Edge(20, (K4, M6))
                )
            ),
            Vertex(
                19,
                V19,
                (
                    Edge(18, (K3, K2))
                )
            ),
            Vertex(
                20,
                V20,
                (
                    Edge(18, (L15, G1)),
                    Edge(21, (G1, L17))
                )
            ),
            Vertex(
                21,
                V21,
                (
                    Edge(17, (G2, G3)),
                    Edge(22, (G3, L19)),
                    Edge(20, (L18, G2))
                )
            ),
            Vertex(
                22,
                V22,
                (
                    Edge(13, (G4, G5)),
                    Edge(23, (G5, L21)),
                    Edge(21, (L20, G4))
                )
            ),
            Vertex(
                23,
                V23,
                (
                    Edge(14, (G6, G7)),
                    Edge(24, (G7, L23)),
                    Edge(22, (L22, G6))
                )
            ),
            Vertex(
                24,
                V24,
                (
                    Edge(15, (G8, L16)),
                    Edge(23, (L24, G8))
                )
            )
        )
    )
