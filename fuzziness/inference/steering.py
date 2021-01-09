import pandas as pd
from scipy.integrate import quad

from constants.fuzziness.names import *
from constants.fuzziness.values import STEERING


def get_functions(label, args, min_arg):
    if label == MIDDLE:
        if min_arg == 1:
            def fx(x):
                if 67.5 < x <= 90:
                    return (x - 67.5) / 22.5
                elif 90 < x <= 112.5:
                    return (112.5 - x) / 22.5
                else:
                    return 0

            def xfx(x):
                if 67.5 < x <= 90:
                    return x * (x - 67.5) / 22.5
                elif 90 < x <= 112.5:
                    return x * (112.5 - x) / 22.5
                else:
                    return 0

            return fx, xfx, min_arg
        else:
            def fx(x):
                if 67.5 < x <= args[0]:
                    return (x - 67.5) / 22.5
                elif args[0] < x <= args[1]:
                    return min_arg
                elif args[1] < x <= 112.5:
                    return (112.5 - x) / 22.5
                else:
                    return 0

            def xfx(x):
                if 67.5 < x <= args[0]:
                    return x * (x - 67.5) / 22.5
                elif args[0] < x <= args[1]:
                    return x * min_arg
                elif args[1] < x <= 112.5:
                    return x * (112.5 - x) / 22.5
                else:
                    return 0

            return fx, xfx, min_arg
    if label == LEFT:
        if min_arg == 1:
            def fx(x):
                if 45 < x <= 67.5:
                    return (x - 45) / 22.5
                elif 67.5 < x <= 90:
                    return (90 - x) / 22.5
                else:
                    return 0

            def xfx(x):
                if 45 < x <= 67.5:
                    return x * (x - 45) / 22.5
                elif 67.5 < x <= 90:
                    return x * (90 - x) / 22.5
                else:
                    return 0

            return fx, xfx, min_arg
        else:
            def fx(x):
                if 45 < x <= args[0]:
                    return (x - 45) / 22.5
                elif args[0] < x <= args[1]:
                    return min_arg
                elif args[1] < x <= 90:
                    return (90 - x) / 22.5
                else:
                    return 0

            def xfx(x):
                if 45 < x <= args[0]:
                    return x * (x - 45) / 22.5
                elif args[0] < x <= args[1]:
                    return x * min_arg
                elif args[1] < x <= 90:
                    return x * (90 - x) / 22.5
                else:
                    return 0

            return fx, xfx, min_arg
    if label == RIGHT:
        if min_arg == 1:
            def fx(x):
                if 90 < x <= 112.5:
                    return (x - 90) / 22.5
                elif 112.5 < x <= 135:
                    return (135 - x) / 22.5
                else:
                    return 0

            def xfx(x):
                if 90 < x <= 112.5:
                    return x * (x - 90) / 22.5
                elif 112.5 < x <= 135:
                    return x * (135 - x) / 22.5
                else:
                    return 0

            return fx, xfx, min_arg
        else:
            def fx(x):
                if 90 < x <= args[0]:
                    return (x - 90) / 22.5
                elif args[0] < x <= args[1]:
                    return min_arg
                elif args[1] < x <= 135:
                    return (135 - x) / 22.5
                else:
                    return 0

            def xfx(x):
                if 90 < x <= args[0]:
                    return x * (x - 90) / 22.5
                elif args[0] < x <= args[1]:
                    return x * min_arg
                elif args[1] < x <= 135:
                    return x * (135 - x) / 22.5
                else:
                    return 0

            return fx, xfx, min_arg
    if label == FAR_LEFT:
        if min_arg == 1:
            def fx(x):
                if x <= 45:
                    return 1
                elif 45 < x <= 67.5:
                    return (67.5 - x) / 22.5
                else:
                    return 0

            def xfx(x):
                if x <= 45:
                    return x
                elif 45 < x <= 67.5:
                    return x * (67.5 - x) / 22.5
                else:
                    return 0

            return fx, xfx, min_arg
        else:
            def fx(x):
                if x <= args[0]:
                    return min_arg
                elif args[0] < x <= 67.5:
                    return (67.5 - x) / 22.5
                else:
                    return 0

            def xfx(x):
                if x <= args[0]:
                    return x * min_arg
                elif args[0] < x <= 67.5:
                    return x * (67.5 - x) / 22.5
                else:
                    return 0

            return fx, xfx, min_arg
    if label == FAR_RIGHT:
        if min_arg == 1:
            def fx(x):
                if x <= 112.5:
                    return 0
                elif 112.5 < x <= 135:
                    return (x - 112.5) / 22.5
                else:
                    return 1

            def xfx(x):
                if x <= 112.5:
                    return 0
                elif 112.5 < x <= 135:
                    return x * (x - 112.5) / 22.5
                else:
                    return x

            return fx, xfx, min_arg
        else:
            def fx(x):
                if x <= 112.5:
                    return 0
                elif 112.5 < x <= args[0]:
                    return (x - 112.5) / 22.5
                else:
                    return min_arg

            def xfx(x):
                if x <= 112.5:
                    return 0
                elif 112.5 < x <= args[0]:
                    return x * (x - 112.5) / 22.5
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
        a, e = quad(xfx, 0, 180)
        b, e = quad(fx, 0, 180)
        angle = a / b
        return angle, weight
