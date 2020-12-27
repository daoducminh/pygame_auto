from constants.coordinates import *


def generate_axes(filename):
    with open(filename, 'w') as f:
        f.write('unit,value\n')
        for i in range(17):
            f.write('X{0},{1}\n'.format(i, eval(f'X{i}')))
        for i in range(31):
            f.write('Y{0},{1}\n'.format(i, eval(f'Y{i}')))


if __name__ == "__main__":
    generate_axes('data/axes.csv')
