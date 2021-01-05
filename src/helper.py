# -*- coding: utf-8 -*-

from pickle import load

from networkx.algorithms.shortest_paths import dijkstra_path


def read_data(filename):
    with open(filename, 'rb') as f:
        return load(f)


def find_shortest_path(graph, source, target):
    return dijkstra_path(graph, source, target)
