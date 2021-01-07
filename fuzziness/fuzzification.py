from constants.fuzziness.values import *


def triangle(x, value):
    if value[0] <= x <= value[1]:
        return (x - value[0]) / (value[1] - value[0])
    if value[1] < x <= value[2]:
        return (value[2] - x) / (value[2] - value[1])
    return 0


def max_left(x, value):
    if x <= value[0]:
        return 1
    if value[0] < x <= value[1]:
        return (value[1] - x) / (value[1] - value[0])
    return 0


def max_right(x, value):
    if x <= value[0]:
        return 0
    if value[0] < x <= value[1]:
        return (x - value[0]) / (value[1] - value[0])
    return 1


def get_deviation_rules(x):
    rs = []
    for i in (LEFT, RIGHT, MIDDLE):
        t = triangle(x, DEVIATION[i])
        if t > 0:
            rs.append((i, t))
    t = max_left(x, DEVIATION[FAR_LEFT])
    if t > 0:
        rs.append((FAR_LEFT, t))
    t = max_right(x, DEVIATION[FAR_RIGHT])
    if t > 0:
        rs.append((FAR_RIGHT, t))
    return rs


def get_light_rules(x):
    rs = []
    for i in (LESS_RED, LESS_GREEN):
        t = triangle(x, LIGHT[i])
        if t > 0:
            rs.append((i, t))
    t = max_left(x, LIGHT[RED])
    if t > 0:
        rs.append((RED, t))
    t = max_right(x, LIGHT[GREEN])
    if t > 0:
        rs.append((GREEN, t))
    return rs


def get_distance_rules(x):
    rs = []
    t = max_left(x, DISTANCE[NEAR])
    if t > 0:
        rs.append((NEAR, t))
    t = max_right(x, DISTANCE[MEDIUM])
    if t > 0:
        rs.append((MEDIUM, t))
    return rs
