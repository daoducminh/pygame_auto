import pandas as pd
from scipy.integrate import quad

from constants.fuzziness.names import *
from constants.fuzziness.values import STEERING


def get_functions(label, args, min_arg):
    if label in (MIDDLE, LEFT, RIGHT):
        a = STEERING[label]
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
    if label == FAR_LEFT:
        a = STEERING[FAR_LEFT]
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
    if label == FAR_RIGHT:
        a = STEERING[FAR_RIGHT]
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


class SteeringDeduction:
    def __init__(self, filename):
        self.rules = pd.read_csv(filename).to_dict(orient='records')

    def get_steering_label(self, value):
        for r in self.rules:
            if r['deviation'] == value:
                return r['steering']

    def deduce(self, rule):
        args = []
        # Get label
        label = self.get_steering_label(rule[0])
        m = rule[1]
        # Inverse function
        if label in (MIDDLE, LEFT, RIGHT):
            a = STEERING[label]
            if m == 1:
                args.append(a[1])
            else:
                args.append((a[1] - a[0]) * m + a[0])
                args.append(a[2] - (a[2] - a[1]) * m)
        if label == FAR_LEFT:
            a = STEERING[FAR_LEFT]
            if m == 1:
                args.append(a[0])
            else:
                args.append(a[1] - (a[1] - a[0]) * m)
        if label == FAR_RIGHT:
            a = STEERING[FAR_RIGHT]
            if m == 1:
                args.append(a[1])
            else:
                args.append((a[1] - a[0]) * m + a[0])
        return label, tuple(args), m

    def calculate(self, label, args, min_arg):
        fx, xfx, weight = get_functions(label, args, min_arg)
        a, e = quad(xfx, 0, 180, maxp1=500, limit=500)
        b, e = quad(fx, 0, 180, maxp1=500, limit=500)
        angle = a / b
        return angle, weight
