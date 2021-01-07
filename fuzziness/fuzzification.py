from constants.fuzziness.values import *


def deviation(x, value):
    if value[0] <= x <= value[1]:
        return (x - value[0]) / (value[1] - value[0])
    if value[1] < x <= value[2]:
        return (value[2] - x) / (value[2] - value[1])
    return 0


def deviation_far_left(x, value):
    if x <= value[0]:
        return 1
    if value[0] < x <= value[1]:
        return (value[1] - x) / (value[1] - value[0])
    return 0


def deviation_far_right(x, value):
    if x <= value[0]:
        return 0
    if value[0] < x <= value[1]:
        return (x - value[0]) / (value[1] - value[0])
    return 1


def get_deviation_rules(x):
    rs = []
    for i in (LEFT, RIGHT, MIDDLE):
        t = deviation(x, DEVIATION[i])
        if t > 0:
            rs.append((i, t))
    t = deviation_far_left(x, DEVIATION[FAR_LEFT])
    if t > 0:
        rs.append((FAR_LEFT, t))
    t = deviation_far_right(x, DEVIATION[FAR_RIGHT])
    if t > 0:
        rs.append((FAR_RIGHT, t))
    return rs


def steering(x, value):
    if value[0] <= x <= value[1]:
        return (x - value[0]) / (value[1] - value[0])
    if value[1] < x <= value[2]:
        return (value[2] - x) / (value[2] - value[1])
    return 0


def light_red(x):
    pass


def light_green(x):
    pass


def light_less_red(x):
    pass


def light_less_green(x):
    pass


def distance_near(x):
    pass


def distance_medium(x):
    pass


def speed_normal(x):
    pass


def speed_slow(x):
    pass


def speed_stop(x):
    pass
