# -*- coding: utf-8 -*-

from math import floor, sqrt
from matplotlib import pyplot as plt
import networkx as nx
from networkx.algorithms.shortest_paths import dijkstra_path
from pickle import load

from constants.coordinates import *
from constants.names import *
from traffic import Vertex, Edge, Board


def init_data(filename):
    with open(filename, 'r') as f:
        return load(f)


# def init_board(data):
#     return Board(
#         {
#             0: Vertex(
#                 center=V0,
#                 edges=(
#                     Edge(1, (A2, B1)),
#                     Edge(6, (B1, L5)),
#                 )
#             )
#         }
#     )
def init_board(data):
    # Coordinate data
    axes = data[AXES]
    coords = data[COORDS]
    # Vertices and edges data
    vertices = data[VERTICES]
    edges = data[EDGES]
    corners = data[CORNERS]

    rs = {}

    for v in vertices:
        center = vertices[CENTER]
        # rs[v[INDEX]] = Vertex(
        #     center
        # )



def calculate_distance(a, b):
    return floor(sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))


def init_graph(board):
    g = nx.Graph()
    vertices = board.vertices

    for key, value in vertices.items():
        g.add_node(key, pos=value.center)
        for e in value.edges:
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
