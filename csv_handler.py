import pandas as pd
import numpy as np
from pickle import dump
from constants import files
from constants.names import *


def generate_axes(filename):
    with open(filename, 'w') as f:
        f.write('{0},{1}\n'.format(UNIT, VALUE))
        for i in range(17):
            f.write('X{0},{1}\n'.format(i, eval(f'X{i}')))
        for i in range(31):
            f.write('Y{0},{1}\n'.format(i, eval(f'Y{i}')))


class DataHandler:
    def __init__(self, axes, coords, vertices, edges, corners, board):
        self.axes_df = pd.read_csv(axes)
        self.coords_df = pd.read_csv(coords)
        self.vertices_df = pd.read_csv(vertices)
        self.edges_df = pd.read_csv(edges)
        self.corners_df = pd.read_csv(corners)
        self.board_df = pd.read_csv(board)

    def to_pickle(self, filename):
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
        with open(filename, 'wb') as f:
            dump(data, f)
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
    data = handler.to_pickle(files.PICKLE_FILE)
    print(data)
