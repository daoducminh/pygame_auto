import pandas as pd
from scipy.integrate import quad

from constants.fuzziness.names import *
from constants.fuzziness.values import SPEED


def get_functions(label, args, min_arg):
    if label == SLOW:
        a = SPEED[SLOW]
        if min_arg == 1:
            def fx(x):
                if x <= a[0]:
                    return 1
                elif a[0] < x <= a[1]:
                    return (a[1] - x) / (a[1] - a[0])
                else:
                    return 0

            def xfx(x):
                if x <= a[0]:
                    return x
                elif a[0] < x <= a[1]:
                    return x * (a[1] - x) / (a[1] - a[0])
                else:
                    return 0

            return fx, xfx, min_arg
        else:
            def fx(x):
                if x <= args[0]:
                    return min_arg
                elif args[0] < x <= a[1]:
                    return (a[1] - x) / (a[1] - a[0])
                else:
                    return 0

            def xfx(x):
                if x <= args[0]:
                    return x * min_arg
                elif args[0] < x <= a[1]:
                    return x * (a[1] - x) / (a[1] - a[0])
                else:
                    return 0

            return fx, xfx, min_arg
    if label == NORMAL:
        a = SPEED[NORMAL]
        if min_arg == 1:
            def fx(x):
                if a[0] < x <= a[1]:
                    return (x - a[0]) / (a[1] - a[0])
                elif a[1] < x <= a[2]:
                    return (a[2] - x) / (a[2] - a[1])
                else:
                    return 0

            def xfx(x):
                if a[0] < x <= a[1]:
                    return x * (x - a[0]) / (a[1] - a[0])
                elif a[1] < x <= a[2]:
                    return x * (a[2] - x) / (a[2] - a[1])
                else:
                    return 0

            return fx, xfx, min_arg
        else:
            def fx(x):
                if a[0] < x <= args[0]:
                    return (x - a[0]) / (a[1] - a[0])
                elif args[0] < x <= args[1]:
                    return min_arg
                elif args[1] < x <= a[2]:
                    return (a[2] - x) / (a[2] - a[1])
                else:
                    return 0

            def xfx(x):
                if a[0] < x <= args[0]:
                    return x * (x - a[0]) / (a[1] - a[0])
                elif args[0] < x <= args[1]:
                    return x * min_arg
                elif args[1] < x <= a[2]:
                    return x * (a[2] - x) / (a[2] - a[1])
                else:
                    return 0

            return fx, xfx, min_arg
    if label == FAST:
        a = SPEED[FAST]
        if min_arg == 1:
            def fx(x):
                if x <= a[0]:
                    return 0
                elif a[0] < x <= a[1]:
                    return (x - a[0]) / (a[1] - a[0])
                else:
                    return 1

            def xfx(x):
                if x <= a[0]:
                    return 0
                elif a[0] < x <= a[1]:
                    return x * (x - a[0]) / (a[1] - a[0])
                else:
                    return x

            return fx, xfx, min_arg
        else:
            def fx(x):
                if x <= a[0]:
                    return 0
                elif a[0] < x <= args[0]:
                    return (x - a[0]) / (a[1] - a[0])
                else:
                    return min_arg

            def xfx(x):
                if x <= a[0]:
                    return 0
                elif a[0] < x <= args[0]:
                    return x * (x - a[0]) / (a[1] - a[0])
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

    def deduce(self, l_rule, d_rule):
        args = []
        # Get label
        label = self.get_speed_label(l_rule[0], d_rule[0])
        m = min(l_rule[1], d_rule[1])
        # Inverse function
        if label == SLOW:
            a = SPEED[SLOW]
            if m == 1:
                args.append(a[0])
            else:
                args.append(a[1] - m * (a[1] - a[0]))
        elif label == NORMAL:
            a = SPEED[NORMAL]
            if m == 1:
                args.append(a[1])
            else:
                args.append(m * (a[1] - a[0]) + a[0])
                args.append(a[2] - m * (a[2] - a[1]))
        elif label == FAST:
            a = SPEED[FAST]
            if m == 1:
                args.append(a[1])
            else:
                args.append(m * (a[1] - a[0]) + a[0])
        elif label == STOP:
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
