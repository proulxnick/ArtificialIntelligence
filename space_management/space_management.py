import random


# class State:
#
#     def __init__(self, grid):
#         self.grid = grid


class Node:

    def __init__(self):
        self.state = list()
        self.parent = None
        self.depth = 0
        self.children = list()  # to be used to create possible child nodes dynamically and append to list
        self.heuristic_value = 0

    def is_at_goal(self,  blank_tiles):
        # the defined goal state for my scope is having all blank tiles at the beginning
        # of the list and all the numbers iterating upward in sequence

        i = 1  # for control
        j = 1  # to count until number of blank tiles
        at_goal = True
        for tile in self.state:
            if j <= blank_tiles:
                if tile == 'x':
                    j += 1
                    continue
                else:
                    j += 1
                    at_goal = False
            else:
                if tile == i:
                    i += 1
                    continue
                else:
                    i += 1
                    at_goal = False

        return at_goal


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


def heuristic_1(grid, blank_tiles):
    # the defined goal state for my scope is having all blank tiles at the beginning
    # of the list and all the numbers iterating upward in sequence

    i = 1  # for control
    j = 1  # to count until number of blank tiles
    count = 0  # num tiles out of place
    for tile in grid:
        if j <= blank_tiles:
            if not tile == 'x':
                count += 1
        else:
            if not tile == i:
                count += 1
            i += 1
        j += 1

    return count


def initiate_grid():
    sequence = [4, 3, 'x', 1, 5, 2]
    # grid = random.shuffle(sequence)

    x_sum = 2
    y_sum = 3
    total = x_sum * y_sum
    blank_tiles = 1

    return sequence, x_sum, y_sum, blank_tiles


def path_exists(path_list, new_node):
    # this is a method to check if the state of the given node exists in the given path
    is_old_state = False

    for node in path_list:
        if new_node.state == node.state:
            is_old_state = True

    return is_old_state


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
                if not new_grid[i] == 'x' \
                   and not new_grid[i - ((2 * x_sum) + 1)] == 'x':
                    new_grid[i], new_grid[i - ((2 * x_sum) + 1)] = new_grid[i - ((2 * x_sum) + 1)], new_grid[i]
                    new_node = create_child(curr_node, new_grid)
                    curr_node.children.append(new_node)

            # move 2 - up 1, left 2
            if j > 1 \
               and k > 2:
                new_grid = copy_list(frontier)
                if not new_grid[i] == 'x' \
                   and not new_grid[i - (x_sum + 2)] == 'x':
                    new_grid[i], new_grid[i - (x_sum + 2)] = new_grid[i - (x_sum + 2)], new_grid[i]
                    new_node = create_child(curr_node, new_grid)
                    curr_node.children.append(new_node)

            # move 3 - up 2, right 1
            if j > 2 \
               and k < x_sum:
                new_grid = copy_list(frontier)
                if not new_grid[i] == 'x' \
                   and not new_grid[i - ((2 * x_sum) - 1)] == 'x':
                    new_grid[i], new_grid[i - ((2 * x_sum) - 1)] = new_grid[i - ((2 * x_sum) - 1)], new_grid[i]
                    new_node = create_child(curr_node, new_grid)
                    curr_node.children.append(new_node)

            # move 4 - up 1, right 2
            if j > 1 \
               and k < (x_sum - 1):
                new_grid = copy_list(frontier)
                if not new_grid[i] == 'x' \
                   and not new_grid[i - (x_sum - 2)] == 'x':
                    new_grid[i], new_grid[i - (x_sum - 2)] = new_grid[i - (x_sum - 2)], new_grid[i]
                    new_node = create_child(curr_node, new_grid)
                    curr_node.children.append(new_node)

            # move 5 - down 2, right 1
            if j < (y_sum - 1) \
               and k < x_sum:
                new_grid = copy_list(frontier)
                if not new_grid[i] == 'x' \
                   and not new_grid[i + ((2 * x_sum) + 1)] == 'x':
                    new_grid[i], new_grid[i + ((2 * x_sum) + 1)] = new_grid[i + ((2 * x_sum) + 1)], new_grid[i]
                    new_node = create_child(curr_node, new_grid)
                    curr_node.children.append(new_node)

            # move 6 - down 1, right 2
            if j < y_sum \
               and k < (x_sum - 1):
                new_grid = copy_list(frontier)
                if not new_grid[i] == 'x' \
                   and not new_grid[i + (x_sum + 2)] == 'x':
                    new_grid[i], new_grid[i + (x_sum + 2)] = new_grid[i + (x_sum + 2)], new_grid[i]
                    new_node = create_child(curr_node, new_grid)
                    curr_node.children.append(new_node)

            # move 7 - down 2, left 1
            if j < (y_sum - 1) \
               and k > 1:
                new_grid = copy_list(frontier)
                if not new_grid[i] == 'x' \
                   and not new_grid[i + ((2 * x_sum) - 1)] == 'x':
                    new_grid[i], new_grid[i + ((2 * x_sum) - 1)] = new_grid[i + ((2 * x_sum) - 1)], new_grid[i]
                    new_node = create_child(curr_node, new_grid)
                    curr_node.children.append(new_node)

            # move 8 - down 1, left 2
            if j < y_sum \
               and k > 2:
                new_grid = copy_list(frontier)
                if not new_grid[i] == 'x' \
                   and not new_grid[i + (x_sum - 2)] == 'x':
                    new_grid[i], new_grid[i + (x_sum - 2)] = new_grid[i + (x_sum - 2)], new_grid[i]
                    new_node = create_child(curr_node, new_grid)
                    curr_node.children.append(new_node)

        # iterate x and y axis markers
        if k == x_sum:
            k = 1
            j += 1
        else:
            k += 1

        i += 1

    return curr_node


def breadth_first():
    grid, x_sum, y_sum, blank_tiles = initiate_grid()
    print grid[0], grid[1], grid[2]
    print grid[3], grid[4], grid[5]
    print grid[6], grid[7], grid[8], '\n'

    node = Node()
    node.state = grid

    path_to_goal = list()
    path_to_goal.append(node)

    while not node.is_at_goal(blank_tiles):
        # initialize the root state and create a new root node with that state
        node = successor_processing(node, x_sum, y_sum)

        # save the slowest run_time across bridge
        cheapest = 0
        curr_node = Node()
        for each_node in node.children:
            if not path_exists(path_to_goal, each_node):
                out_of_place = heuristic_1(each_node.state, blank_tiles)
                if cheapest == 0 \
                   or out_of_place < cheapest:
                    cheapest = out_of_place
                    curr_node = each_node  # current node now has cheapest run time at it's depth

        # append the node with the cheapest crossing time to the final path to the goal state
        path_to_goal.append(curr_node)
        node = curr_node  # get successors / fringe from the cheapest node at this state

    print '\nBreadth-first search chosen'
    print 'Total number of moves: ' + str(node.depth)
    return path_to_goal


def depth_first():
    grid, x_sum, y_sum, blank_tiles = initiate_grid()
    print grid[0], grid[1], grid[2]
    print grid[3], grid[4], grid[5]
    print grid[6], grid[7], grid[8], '\n'

    path_to_goal = list()
    node = Node()
    node.state = grid
    path_to_goal.append(node)
    stack = list()  # use a stack for dfs
    already_processed = False

    while not node.is_at_goal(blank_tiles):
        if not already_processed:
            node = successor_processing(node, x_sum, y_sum)
            already_processed = True
            stack.extend(node.children)  # add the children to the top of the stack

        curr_node = stack.pop()  # take the latest child addition as current node
        if not path_exists(path_to_goal, curr_node):
            already_processed = False
            path_to_goal.append(curr_node)

        node = curr_node  # use this current node to get it's successors / fringe

    print '\nDepth-first search chosen'
    return path_to_goal


def a_star():
    grid, x_sum, y_sum, blank_tiles = initiate_grid()
    print grid[0], grid[1],
    print grid[2], grid[3],
    print grid[4], grid[5], '\n'

    node = Node()
    node.state = grid

    path_to_goal = list()
    closed = list()
    transplanted = list()
    path_to_goal.append(node)

    while not node.is_at_goal(blank_tiles):
        # initialize the root state and create a new root node with that state
        node = successor_processing(node, x_sum, y_sum)

        # save the slowest run_time across bridge
        cheapest = 0
        curr_node = Node()
        for each_node in node.children:
            if not path_exists(path_to_goal, each_node):
                out_of_place = heuristic_1(each_node.state, blank_tiles)
                if cheapest == 0 \
                        or out_of_place < cheapest:
                    cheapest = out_of_place
                    curr_node = each_node  # current node now has cheapest run time at it's depth

        for each_node in node.children:
            cost = heuristic_1(each_node.state, blank_tiles)
            if not each_node.state == curr_node.state:
                each_node.heuristic_value = cost
                closed.append(each_node)
            else:
                curr_node.heuristic_value = cost

        transplant = False
        scope_changes = 0
        if path_exists(closed, curr_node):
            for closed_node in closed:
                if closed_node.state == curr_node.state \
                   and closed_node.heuristic_value <= curr_node.heuristic_value \
                   and closed_node.depth < curr_node.depth\
                   and closed_node.state not in transplanted\
                   and curr_node.state not in transplanted:
                    i = closed_node.depth
                    path_to_goal = path_to_goal[:i]
                    path_to_goal.append(closed_node)
                    transplant = True
                    transplanted.append(closed_node.state)
                    transplanted.append(curr_node.state)
                    scope_changes += 1
                    break

        if not transplant:
            # append the node with the cheapest crossing time to the final path to the goal state
            path_to_goal.append(curr_node)

        node = path_to_goal[-1]  # get successors / fringe from the cheapest node at this state

    print '\nA star search chosen'
    print 'Total number of moves: ' + str(node.depth)
    print 'Total number of transplants of children (changes of scope): ' + str(scope_changes)
    return path_to_goal


def print_path(path):
    for node in path:
        print node.state[0], node.state[1],
        print node.state[2], node.state[3],
        print node.state[4], node.state[5], '\n'


# to be called at top level
def main():
    path = a_star()
    print_path(path)


# top level code
if __name__ == '__main__':
    main()
