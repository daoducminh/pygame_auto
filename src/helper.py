# -*- coding: utf-8 -*-

from math import floor, sqrt
from pickle import load

import networkx as nx
from matplotlib import pyplot as plt
from networkx.algorithms.shortest_paths import dijkstra_path

from constants.names import *
from .traffic import Vertex, Corner, Board


def init_data(filename):
    with open(filename, 'rb') as f:
        return load(f)


def init_board(data):
    # Coordinate data
    coords = data[COORDS]
    # Vertices and edges data
    vertices = data[VERTICES]
    edges = data[EDGES]
    corners = data[CORNERS]
    # Map board
    board = data[BOARD]

    rs = {}

    # Map board
    map_board = []
    for b in board:
        map_board.append(tuple(
            coords[i] for i in b
        ))

    # Edges
    for e in edges:
        e[BODY] = tuple(coords[i] for i in e[BODY])

        blocked = []
        for b in e[BLOCKED]:
            blocked.append(tuple(
                coords[i] for i in b
            ))
        e[BLOCKED] = tuple(blocked)

    # Vertices
    for v in vertices:
        v_index = v[INDEX]
        cs = []

        for c in corners:
            if v_index == c[FROM]:
                cs.append(Corner(
                    c[TO],
                    tuple(coords[i] for i in c[CORNERS])
                ))

        blocked = []
        for b in v[BLOCKED]:
            blocked.append(tuple(
                coords[i] for i in b
            ))

        es = []
        for e in edges:
            if v_index in e[VERTICES]:
                es.append(e)

        rs[v_index] = Vertex(
            center=coords[v[CENTER]],
            corners=tuple(cs),
            body=tuple(coords[i] for i in v[BODY]),
            blocked=blocked,
            edges=tuple(es)
        )
    return Board(rs, tuple(map_board))


def calculate_distance(a, b):
    return floor(sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))


def init_graph(board):
    g = nx.Graph()
    vertices = board.vertices

    for key, value in vertices.items():
        g.add_node(key, pos=value.center)
        for e in value.corners:
            g.add_edge(key, e.neighbor)
    for e in list(g.edges):
        u, v = e
        g.edges[u, v]['weight'] = calculate_distance(
            vertices[u].center,
            vertices[v].center
        )
    return g


def find_shortest_path(graph, source, target):
    return dijkstra_path(graph, source, target)


def draw_graph(graph):
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos=pos, with_labels=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.savefig('test.png')
