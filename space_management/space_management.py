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

    x_sum = 3
    y_sum = 3
    total = x_sum * y_sum
    blank_tiles = 1

    return grid, x_sum, y_sum, blank_tiles


def successor_processing(curr_node, x_sum, y_sum, blank_tiles):
    frontier = curr_node.grid

    i = 0  # list index
    j = 1  # the y axis
    k = 1  # the x axis
    for curr_tile in frontier:
        if curr_tile == 'x':  # 8 possible moves for the blank tile
            # move 1 - northwest
            if not j == 1 \
               and not k == 1:
                frontier[i], frontier[i - (x_sum + 1)] = frontier[i - (x_sum + 1)], frontier[i]

            # move 2 - north
            if not j == 1:
                frontier[i], frontier[i - x_sum] = frontier[i - x_sum], frontier[i]

            # move 3 - northeast
            if not j == 1 \
               and not k == x_sum:
                frontier[i], frontier[i - (x_sum - 1)] = frontier[i - (x_sum - 1)], frontier[i]

            # move 4 - east
            if not k == x_sum:
                frontier[i], frontier[i + 1] = frontier[i + 1], frontier[i]

            # move 5 - southeast
            if not j == y_sum \
               and not k == x_sum:
                frontier[i], frontier[i + (x_sum + 1)] = frontier[i + (x_sum + 1)], frontier[i]

            # move 6 - south
            if not j == y_sum:
                frontier[i], frontier[i + x_sum] = frontier[i + x_sum], frontier[i]

            # move 7 - southwest
            if not j == y_sum \
               and not k == 1:
                frontier[i], frontier[i + (x_sum - 1)] = frontier[i + (x_sum - 1)], frontier[i]

            # move 8 - west
            if not k == 1:
                frontier[i], frontier[i - 1] = frontier[i - 1], frontier[i]


# to be called at top level
def main():
    pass


# top level code
if __name__ == '__main__':
    main()
