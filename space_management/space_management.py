import random


class State:

    def __init__(self, grid):
        self.grid = grid


class Node:

    def __init__(self):
        self.state = None
        self.parent = None
        self.depth = 0
        self.children = list()  # to be used to create possible child nodes dynamically and append to list
        self.heuristic_value = 0


def initiate_grid():
    sequence = [1, 2, 3, 4, 5, 6, 7, 8, 'x']
    grid = random.shuffle(sequence)

    return grid


def successor_processing(grid):
    pass


# to be called at top level
def main():
    pass


# top level code
if __name__ == '__main__':
    main()
