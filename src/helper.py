# -*- coding: utf-8 -*-

from pickle import load

from networkx.algorithms.shortest_paths import dijkstra_path

from constants.car import MIN_ANGLE


def read_data(filename):
    with open(filename, 'rb') as f:
        return load(f)


def find_shortest_path(graph, source, target):
    return dijkstra_path(graph, source, target)


def handle_angle(angle):
    t = abs(angle)
    if t > 60:
        if angle > 0:
            return MIN_ANGLE * 1.7
        else:
            return -MIN_ANGLE * 1.7
    if t > 40:
        if angle > 0:
            return MIN_ANGLE * 1.3
        else:
            return -MIN_ANGLE * 1.3
    elif t > 20:
        if angle > 0:
            return MIN_ANGLE
        else:
            return -MIN_ANGLE
    else:
        return angle
