import random


# class State:
#
#     def __init__(self, grid):
#         self.grid = grid


class Node:

    def __init__(self):
        self.state = None
        self.parent = None
        self.depth = 0
        self.children = list()  # to be used to create possible child nodes dynamically and append to list
        self.heuristic_value = 0


def copy_list(old_list):
    # used to copy contents of one list and create another list
    new_list = list()

    for i in old_list:
        new_list.append(i)

    return new_list


def create_child(curr_node, new_grid):
    # create a new node to be appended to the current node's list of children
    new_node = Node()
    new_node.parent = curr_node
    new_node.state = new_grid
    new_node.depth = curr_node.depth + 1

    return new_node


def is_at_goal(grid, blank_tiles):
    # the defined goal state for my scope is having all blank tiles at the beginning
    # of the list and all the numbers iterating upward in sequence
    i = 1  # for control
    j = 1  # to count until number of blank tiles
    at_goal = True
    for tile in grid:
        if not j == blank_tiles:
            if tile == 'x':
                continue
            else:
                at_goal = False
                break
        else:
            if tile == i:
                i += 1
                continue
            else:
                at_goal = False
                break

    return at_goal


def initiate_grid():
    sequence = [1, 2, 3, 4, 5, 6, 7, 8, 'x']
    grid = random.shuffle(sequence)

    x_sum = 3
    y_sum = 3
    total = x_sum * y_sum
    blank_tiles = 1

    return grid, x_sum, y_sum, blank_tiles


def successor_processing(curr_node, x_sum, y_sum):
    frontier = curr_node.state

    i = 0  # list index
    j = 1  # the y axis
    k = 1  # the x axis
    for curr_tile in frontier:
        if curr_tile == 'x':  # 8 possible moves for the blank tile
            # move 1 - northwest
            if not j == 1 \
               and not k == 1:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i - (x_sum + 1)] = new_grid[i - (x_sum + 1)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 2 - north
            if not j == 1:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i - x_sum] = new_grid[i - x_sum], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 3 - northeast
            if not j == 1 \
               and not k == x_sum:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i - (x_sum - 1)] = new_grid[i - (x_sum - 1)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 4 - east
            if not k == x_sum:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i + 1] = new_grid[i + 1], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 5 - southeast
            if not j == y_sum \
               and not k == x_sum:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i + (x_sum + 1)] = new_grid[i + (x_sum + 1)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 6 - south
            if not j == y_sum:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i + x_sum] = new_grid[i + x_sum], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 7 - southwest
            if not j == y_sum \
               and not k == 1:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i + (x_sum - 1)] = new_grid[i + (x_sum - 1)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 8 - west
            if not k == 1:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i - 1] = new_grid[i - 1], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

        else:  # is an integer tile - 8 possible moves
            # move 1 - up 2, left 1
            if j > 2 \
               and k > 1:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i - ((2 * x_sum) + 1)] = new_grid[i - ((2 * x_sum) + 1)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 2 - up 1, left 2
            if j > 1 \
               and k > 2:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i - (x_sum + 2)] = new_grid[i - (x_sum + 2)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 3 - up 2, right 1
            if j > 2 \
               and k < x_sum:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i - ((2 * x_sum) - 1)] = new_grid[i - ((2 * x_sum) - 1)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 4 - up 1, right 2
            if j > 1 \
               and k < (x_sum - 1):
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i - (x_sum - 2)] = new_grid[i - (x_sum - 2)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 5 - down 2, right 1
            if j < (y_sum - 1) \
               and k < x_sum:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i + ((2 * x_sum) + 1)] = new_grid[i + ((2 * x_sum) + 1)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 6 - down 1, right 2
            if j < y_sum \
               and k < (x_sum - 1):
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i + (x_sum + 2)] = new_grid[i + (x_sum + 2)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 7 - down 2, left 1
            if j < (y_sum - 1) \
               and k > 1:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i + ((2 * x_sum) - 1)] = new_grid[i + ((2 * x_sum) - 1)], new_grid[i]
                new_node = create_child(curr_node, new_grid)
                curr_node.children.append(new_node)

            # move 8 - down 1, left 2
            if j < y_sum \
               and k > 2:
                new_grid = copy_list(frontier)
                new_grid[i], new_grid[i + (x_sum - 2)] = new_grid[i + (x_sum - 2)], new_grid[i]

        # iterate x and y axis markers
        if k == x_sum:
            k = 0
            j += 1
        else:
            k += 1

        i += 1


# to be called at top level
def main():
    pass


# top level code
if __name__ == '__main__':
    main()
