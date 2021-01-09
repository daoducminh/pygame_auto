from .names import *

DEVIATION = {
    MIDDLE: (0.4, 0.5, 0.6),
    LEFT: (0.3, 0.4, 0.5),
    RIGHT: (0.5, 0.6, 0.7),
    FAR_LEFT: (0.3, 0.4),
    FAR_RIGHT: (0.6, 0.7)
}

LIGHT = {
    RED: (17, 19),
    GREEN: (21, 23),
    LESS_RED: (17, 19, 21),
    LESS_GREEN: (19, 21, 23)
}

DISTANCE = {
    NEAR: (10, 30),
    MEDIUM: (20, 50)
}

SPEED = {
    SLOW: (1, 3),
    NORMAL: (2, 3, 4),
    FAST: (3, 7)
}

STEERING = {
    MIDDLE: (67.5, 90, 112.5),
    LEFT: (45, 67.5, 90),
    RIGHT: (90, 112.5, 135),
    FAR_LEFT: (45, 67.5),
    FAR_RIGHT: (112.5, 135)
}
