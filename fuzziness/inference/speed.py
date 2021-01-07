import pandas as pd
from scipy.integrate import quad

from constants.fuzziness.names import *


def get_functions(label, args, min_arg):
    if label == SLOW:
        if min_arg == 1:
            def fx(x):
                if x <= 3:
                    return 1
                elif 3 < x <= 4:
                    return 4 - x
                else:
                    return 0

            def xfx(x):
                if x <= 3:
                    return x
                elif 3 < x <= 4:
                    return x * (4 - x)
                else:
                    return 0

            return fx, xfx, min_arg
        else:
            def fx(x):
                if x <= args[0]:
                    return min_arg
                elif args[0] < x <= 4:
                    return 4 - x
                else:
                    return 0

            def xfx(x):
                if x <= args[0]:
                    return x * min_arg
                elif args[0] < x <= 4:
                    return x * (4 - x)
                else:
                    return 0

            return fx, xfx, min_arg
    if label == NORMAL:
        if min_arg == 1:
            def fx(x):
                if x <= 3:
                    return 0
                elif 3 < x <= 4:
                    return x - 3
                else:
                    return 1

            def xfx(x):
                if x <= 3:
                    return 0
                elif 3 < x <= 4:
                    return x * (x - 3)
                else:
                    return x

            return fx, xfx, min_arg
        else:
            def fx(x):
                if x <= 3:
                    return 0
                elif 3 < x <= args[0]:
                    return x - 3
                else:
                    return min_arg

            def xfx(x):
                if x <= 3:
                    return 0
                elif 3 < x <= args[0]:
                    return x * (x - 3)
                else:
                    return x * min_arg

            return fx, xfx, min_arg


class SpeedDeduction:
    def __init__(self, filename):
        self.rules = pd.read_csv(filename).to_dict(orient='records')

    def get_speed_label(self, light, distance):
        for r in self.rules:
            if r['light'] == light and r['distance'] == distance:
                return r['speed']

    def deduce(self, rule):
        args = []
        # Get label
        label = self.get_speed_label(rule[0], rule[1])
        m = rule[2]
        # Inverse function
        if label == SLOW:
            if m == 1:
                args.append(3)
            else:
                args.append(4 - m)
        if label == NORMAL:
            if m == 1:
                args.append(4)
            else:
                args.append(m + 3)
        if label == STOP:
            args.append(0)
        return label, tuple(args), m

    def calculate(self, label, args, min_arg):
        if label == STOP:
            return 0, 1
        else:
            fx, xfx, weight = get_functions(label, args, min_arg)
            a, e = quad(xfx, 0, 5)
            b, e = quad(fx, 0, 5)
            speed = a / b
            return speed, weight
