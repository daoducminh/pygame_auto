import pandas as pd
import numpy as np
from pickle import dump
from constants import files


def generate_axes(filename):
    with open(filename, 'w') as f:
        f.write('unit,value\n')
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
        axes = {
            i['unit']: i['value'] for i in self.axes_df.to_dict(orient='records')
        }
        coords = {
            i['point']: (i['x'], i['y']) for i in self.coords_df.to_dict(orient='records')
        }
        board = tuple(tuple(i.split('|')) for i in self.board_df.to_list())
        corners = tuple(self.corners_df.to_dict(orient='records'))
        for i in corners:
            i['corners'] = tuple(i['corners'].split('|'))
        edges = tuple(self.edges_df.to_dict(orient='records'))
        for i in edges:
            i['vertices'] = tuple(int(j) for j in i['vertices'].split('|'))
            i['body'] = tuple(i['body'].split('|'))
            i['blocked'] = tuple(tuple(j.split('-'))
                                 for j in i['blocked'].split('|'))
        vertices = tuple(self.vertices_df.to_dict(orient='records'))
        for i in vertices:
            i['body'] = tuple(i['body'].split('|'))
            i['blocked'] = tuple(tuple(
                j.split('-')) for j in i['blocked'].split('|')) if i['blocked'] else tuple()
        data = {
            'axes': axes,
            'board': board,
            'coords': coords,
            'corners': corners,
            'edges': edges,
            'vertices': vertices
        }
        with open(filename, 'wb') as f:
            dump(data, f)


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
    handler.to_pickle(files.PICKLE_FILE)
