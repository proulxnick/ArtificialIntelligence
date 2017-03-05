import random


class BadStateException(Exception):

    def __init__(self, message):
        self.message = message


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


def heuristic_2(grid, blank_tiles):
    # get the cumulative distance every tile is from it's endpoint and return it

    total_distance = 0
    for tile in grid:
        if tile == 'x':
            continue
        curr_index = grid.index(tile)
        if curr_index == blank_tiles + (tile - 1):
            continue
        else:
            difference = blank_tiles + (tile - 1) - curr_index
            if difference < 0:
                difference = (difference * -1)
            total_distance += difference

    return total_distance


def initiate_grid():
    # get the user to specify the grid size and number of tiles

    valid = False
    x_sum = 0
    y_sum = 0
    blank_tiles = 0
    total = 0
    print "Enter the X and Y coordinates to make up the grid size (e.g X=3 and Y=3 for a 3x3 grid matrix)"
    while not valid:
        x_sum = input("X coordinates: ")
        y_sum = input("Y coordinates: ")

        print '\n'

        blank_tiles = input("Enter number of blank spaces in the grid: ")
        total = x_sum * y_sum
        if x_sum > 1 \
           and y_sum > 1 \
           and blank_tiles <= total:
            valid = True
        else:
            print 'You must have an X and Y axis greater than 1, and a valid number of blank tiles - try again'

    i = 1
    k = 1
    sequence = list()
    while i <= total:
        if i <= blank_tiles:
            sequence.append('x')
        else:
            sequence.append(k)
            k += 1
        i += 1

    random.shuffle(sequence)  # randomize the matrix

    print 'The original grid is: '
    i = 1
    j = 0
    while j < total:
        print sequence[j],
        if not i == x_sum:
            i += 1
        else:
            print''
            i = 1
        j += 1

    print '\n'

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

        elif not curr_tile == 'x':  # is an integer tile - 8 possible moves
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
                    curr_node = each_node  # current node now has cheapest heuristic value

        # append the node with the cheapest crossing time to the final path to the goal state
        path_to_goal.append(curr_node)
        node = curr_node  # get successors / fringe from the cheapest node at this state

    print '\nBreadth-first search chosen'
    print 'Total number of moves: ' + str(node.depth)
    return path_to_goal, x_sum, y_sum


def depth_first():
    grid, x_sum, y_sum, blank_tiles = initiate_grid()

    path_to_goal = list()
    node = Node()
    node.state = grid
    node.heuristic_value = heuristic_1(node.state, blank_tiles)
    path_to_goal.append(node)
    stack = list()  # use a stack for dfs
    visited = list()
    already_processed = False

    while not node.is_at_goal(blank_tiles):
        if not already_processed:
            node = successor_processing(node, x_sum, y_sum)
            already_processed = True
            stack.extend(node.children)  # add the children to the top of the stack

        curr_node = stack.pop()  # take the latest child addition as current node
        out_of_place = heuristic_1(curr_node.state, blank_tiles)
        curr_node.heuristic_value = out_of_place
        if not path_exists(path_to_goal, curr_node) \
           and curr_node.heuristic_value <= path_to_goal[-1].heuristic_value \
           and not path_exists(visited, curr_node):
            already_processed = False
            path_to_goal.append(curr_node)
            visited.append(node)

        if len(stack) > 1:
            node = curr_node  # use this current node to get it's successors / fringe
        elif len(stack) <= 1 and not node.is_at_goal(blank_tiles):
            path_to_goal = path_to_goal[:1]
            node = path_to_goal[-1]

    print '\nDepth-first search chosen'
    print 'Total number of moves: ' + str(node.depth)
    return path_to_goal, x_sum, y_sum


def a_star():
    grid, x_sum, y_sum, blank_tiles = initiate_grid()
    node = Node()
    node.state = grid

    path_to_goal = list()
    closed = list()
    transplanted = list()
    path_to_goal.append(node)
    scope_changes = 0

    while not node.is_at_goal(blank_tiles):
        # initialize the root state and create a new root node with that state
        node = successor_processing(node, x_sum, y_sum)

        # will be the cheapest heuristic value
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

        transplant = False  # to check if a node's children were transplanted for change of scope
        if path_exists(closed, curr_node):
            for closed_node in closed:
                if closed_node.state == curr_node.state \
                   and closed_node.heuristic_value <= curr_node.heuristic_value \
                   and closed_node.depth < curr_node.depth\
                   and closed_node.state not in transplanted\
                   and curr_node.state not in transplanted:
                    # there is a better option in the list of nodes visited, transplant the children
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
    return path_to_goal, x_sum, y_sum


def print_path(path, x_sum, y_sum):
    # used to print out the states of each node as the specified matrix size
    total = x_sum * y_sum
    for node in path:
        i = 1
        j = 0
        while j < total:
            print node.state[j],
            if not i == x_sum:
                i += 1
            else:
                print''
                i = 1
            j += 1
        print '\n'


# to be called at top level
def main():
    # path, x, y = breadth_first()
    # path, x, y = a_star()
    path, x, y = depth_first()
    print_path(path, x, y)


# top level code
if __name__ == '__main__':
    main()
