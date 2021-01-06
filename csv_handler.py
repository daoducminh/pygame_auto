from math import floor, sqrt
from pickle import dump

import matplotlib.path as plt_path
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sympy import Segment

from constants import files
from constants.names import *
from src.traffic import Vertex, Corner, Board, Edge


def to_pickle(data, filename):
    with open(filename, 'wb') as f:
        dump(data, f)


def calculate_distance(a, b):
    return floor(sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))


def draw_graph(graph):
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos=pos, with_labels=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.savefig('test.png')


def generate_axes(filename):
    with open(filename, 'w') as f:
        f.write('{0},{1}\n'.format(UNIT, VALUE))
        for i in range(17):
            f.write('X{0},{1}\n'.format(i, eval(f'X{i}')))
        for i in range(31):
            f.write('Y{0},{1}\n'.format(i, eval(f'Y{i}')))


def get_board(data):
    coords = data[COORDS]
    # Vertices and edges data
    vertices_data = data[VERTICES]
    edges_data = data[EDGES]
    corners_data = data[CORNERS]
    # Map board
    board_data = data[BOARD]

    vertices = {}

    # Map board
    map_board = []
    for b in board_data:
        map_board.append(tuple(
            coords[i] for i in b
        ))

    # Edges
    edges = []
    for e in edges_data:
        body = tuple(coords[i] for i in e[BODY])

        blocked = []
        segments = []
        for b in e[BLOCKED]:
            t = tuple(
                coords[i] for i in b
            )
            blocked.append(t)
            segments.append(Segment(*t))
        edges.append(Edge(
            vertices=e[VERTICES],
            body=body,
            blocked=blocked,
            segments=segments,
            box=plt_path.Path(np.array(body))
        ))

    # Vertices
    for v in vertices_data:
        v_index = v[INDEX]
        cs = []

        for c in corners_data:
            if v_index == c[FROM]:
                cs.append(Corner(
                    c[TO],
                    tuple(coords[i] for i in c[CORNERS])
                ))

        blocked = []
        segments = []
        for b in v[BLOCKED]:
            t = tuple(
                coords[i] for i in b
            )
            blocked.append(t)
            segments.append(Segment(*t))

        es = []
        for e in edges:
            if v_index in e.vertices:
                es.append(e)
        body = tuple(coords[i] for i in v[BODY])

        vertices[v_index] = Vertex(
            center=coords[v[CENTER]],
            corners=tuple(cs),
            body=body,
            blocked=blocked,
            edges=tuple(es),
            segments=segments,
            box=plt_path.Path(np.array(body))
        )
    return Board(vertices, edges, tuple(map_board))


def get_graph(board):
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


class DataHandler:
    def __init__(self, axes, coords, vertices, edges, corners, board):
        self.axes_df = pd.read_csv(axes)
        self.coords_df = pd.read_csv(coords)
        self.vertices_df = pd.read_csv(vertices)
        self.edges_df = pd.read_csv(edges)
        self.corners_df = pd.read_csv(corners)
        self.board_df = pd.read_csv(board)

    def preprocess(self):
        # Axes
        axes = {
            i[UNIT]: i[VALUE] for i in self.axes_df.to_dict(orient='records')
        }
        # Coords
        coords = {
            i[POINT]: (i[X], i[Y]) for i in self.coords_df.to_dict(orient='records')
        }
        # Board
        board = tuple(
            tuple(i.split('|'))
            for i in self.board_df.loc[:, 'path'].to_list()
        )
        corners = tuple(self.corners_df.to_dict(orient='records'))
        for i in corners:
            i[CORNERS] = tuple(i[CORNERS].split('|'))
        # Edges
        edges = tuple(self.edges_df.to_dict(orient='records'))
        for i in edges:
            i[VERTICES] = tuple(int(j) for j in i[VERTICES].split('|'))
            i[BODY] = tuple(i[BODY].split('|'))
            i[BLOCKED] = tuple(
                tuple(j.split('-')) for j in i[BLOCKED].split('|')
            )
        # Vertices
        vertices = tuple(self.vertices_df.replace(
            np.NaN, False).to_dict(orient='records'))
        for i in vertices:
            i[BODY] = tuple(i[BODY].split('|'))
            i[BLOCKED] = tuple(tuple(
                j.split('-')) for j in i[BLOCKED].split('|')) if i[BLOCKED] else tuple()

        # Merge axes to coords
        for k, v in coords.items():
            coords[k] = (axes[v[0]], axes[v[1]])

        data = {
            BOARD: board,
            COORDS: coords,
            CORNERS: corners,
            EDGES: edges,
            VERTICES: vertices
        }
        return data


if __name__ == "__main__":
    # generate_axes('data/axes.csv')
    handler = DataHandler(
        files.AXES,
        files.COORDS,
        files.VERTICES,
        files.EDGES,
        files.CORNERS,
        files.BOARD
    )

    data = handler.preprocess()
    to_pickle(data, files.DATA_FILE)

    board = get_board(data)
    to_pickle(board, files.BOARD_FILE)

    graph = get_graph(board)
    to_pickle(graph, files.GRAPH_FILE)
