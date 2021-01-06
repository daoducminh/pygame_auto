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
    if value[0] <= x:
        return 0
    if value[0] < x <= value[1]:
        return (x - value[0]) / (value[1] - value[0])
    return 1


def steering(x):
    pass


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
