import random
import math


class BadStateException(Exception):

    def __init__(self, message):
        self.message = message


class Node:

    def __init__(self):
        self.state = list()
        self.parent = None
        self.depth = 0
        self.children = list()
        self.heuristic_value = 0


def copy_list(old_list):
    # used to copy contents of one list and create another list

    new_list = list()
    for i in old_list:
        new_list.append(i)

    return new_list


def randomize_cube():
    valid_size = False
    initial_state = list()
    size = 0

    # get the user to input the degree of the cube
    while not valid_size:
        size = input("Enter the degree/size cube you wish to solve (e.g 3 = 3x3 Rubik's Cube)")
        if size > 1:
            valid_size = True
        else:
            print "Cube size must be greater than 1"

    # now populate the list of tiles which will be the original state
    count1 = 0
    count2 = 0
    i = 1
    while count1 < 6:
        while count2 < math.pow(size, 2):
            initial_state.append(i)
            count2 += 1
        count1 += 1
        count2 = 0
        i += 1

    random.shuffle(initial_state)  # randomize the order of the cube

    return initial_state


def process_moves(curr_node, cube_size):

    # at any point in time there will be 3*cube_size number of new moves
    # this function calculates and returns all possible moves and returns
    # each as a new state in a newly constructed node

    cube_state = curr_node.state  # state passed in - this will be copied and manipulated
    side_total = math.pow(cube_size, 2)

    # move up front
    row = 1
    column = 1
    i = side_total * 5  # first index at front of cube
    j = side_total  # first index at top of cube
    k = side_total * 4  # first index at back of cube
    l = side_total * 3  # first index at bottom of cube
    while row <= cube_size:
        new_state = copy_list(cube_state)
        while column <= cube_size:
            new_state[j] = cube_state[i]  # front -> top
            new_state[k] = cube_state[j]  # top -> back
            new_state[l] = cube_state[k]  # back -> bottom
            new_state[i] = cube_state[l]  # bottom -> front

            i += cube_size
            j += cube_size
            k += cube_size
            l += cube_size
            column += 1
        # create new node with new_state
        new_node = Node()
        new_node.state = new_state
        new_node.parent = curr_node
        new_node.depth = curr_node.depth + 1
        curr_node.children.append(new_node)
        row += 1


# to be called at top level
def main():
    state = randomize_cube()
    print state

# top level code
if __name__ == '__main__':
    main()
