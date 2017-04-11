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

    def is_at_goal(self, state):
        complete = True
        i = 1
        face_size = len(state) / 6
        for tile in state:
            if i <= face_size \
                    and not tile == 1:
                complete = False
                break
            elif face_size * 2 >= i > face_size \
                    and not tile == 2:
                complete = False
                break
            elif face_size * 3 >= i > face_size * 2 \
                    and not tile == 3:
                complete = False
                break
            elif face_size * 4 >= i > face_size * 3 \
                    and not tile == 4:
                complete = False
                break
            elif face_size * 5 >= i > face_size * 4 \
                    and not tile == 5:
                complete = False
                break
            elif len(state) >= i > face_size * 5 \
                    and not tile == 6:
                complete = False
                break
            i += 1

        return complete


def copy_list(old_list):
    # used to copy contents of one list and create another list

    new_list = list()
    for i in old_list:
        new_list.append(i)

    return new_list


def out_of_place(node):
    # heuristic to find number of nodes out of goal state positioning
    i = 1
    count = 0
    face_size = len(node.state) / 6
    for tile in node.state:
        if i <= face_size \
           and not tile == 1:
            count += 1
        elif face_size * 2 >= i > face_size \
                and not tile == 2:
            count += 1
        elif face_size * 3 >= i > face_size * 2 \
                and not tile == 3:
            count += 1
        elif face_size * 4 >= i > face_size * 3 \
                and not tile == 4:
            count += 1
        elif face_size * 5 >= i > face_size * 4 \
                and not tile == 5:
            count += 1
        elif len(node.state) >= i > face_size * 5 \
                and not tile == 6:
            count += 1
        i += 1

    node.heuristic_value = count
    return node


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

    return initial_state, size


def rotate_counterclockwise(face):
    new_face = list()

    face = zip(*face)[::-1]
    for row in face:
        for value in row:
            new_face.append(value)

    return new_face


def rotate_clockwise(face):
    new_face = list()

    face = zip(*face[::-1])
    for row in face:
        for value in row:
            new_face.append(value)

    return new_face


def process_moves(curr_node, cube_size):

    # at any point in time there will be 3*cube_size number of new moves
    # this function calculates and returns all possible moves and returns
    # each as a new state in a newly constructed node

    cube_state = curr_node.state  # state passed in - this will be copied and manipulated
    side_total = int(math.pow(cube_size, 2))
    used_states = list()

    # move up front
    row = 1
    i = side_total * 5  # first index at front of cube
    j = side_total  # first index at top of cube
    k = side_total * 4  # first index at back of cube
    l = side_total * 3  # first index at bottom of cube
    m = 0  # first index at left of cube
    n = side_total * 2  # first index at right of cube
    while row <= cube_size:
        new_state = copy_list(cube_state)
        column = 0
        while column < cube_size:
            new_state[j] = cube_state[i]  # front -> top
            new_state[k] = cube_state[j]  # top -> back
            new_state[l] = cube_state[k]  # back -> bottom
            new_state[i] = cube_state[l]  # bottom -> front
            if column == 0:  # left side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while m < side_total:
                        new_row.append(cube_state[m])
                        m += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_counterclockwise(new_face)
                m = 0  # first index at left of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if column == cube_size - 1:  # right side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while n < side_total:
                        new_row.append(cube_state[n])
                        n += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_clockwise(new_face)
                n = side_total * 2  # first index at right of cube
                for value in rotated_face:
                    new_state[n] = value
                    n += 1

            i += cube_size
            j += cube_size
            k += cube_size
            l += cube_size
            column += 1

        # create new node with new_state if not already been created
        if new_state not in used_states:
            new_node = Node()
            new_node.state = new_state
            new_node.parent = curr_node
            new_node.depth = curr_node.depth + 1
            curr_node.children.append(new_node)
            used_states.append(new_state)
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = side_total * 3  # first index at bottom of cube
        i += row
        j += row
        k += row
        l += row
        row += 1

    # move down front
    row = 1
    i = side_total * 5  # first index at front of cube
    j = side_total  # first index at top of cube
    k = side_total * 4  # first index at back of cube
    l = side_total * 3  # first index at bottom of cube
    m = 0  # first index at left of cube
    n = side_total * 2  # first index at right of cube
    while row <= cube_size:
        new_state = copy_list(cube_state)
        column = 0
        while column < cube_size:
            new_state[i] = cube_state[l]  # front -> bottom
            new_state[l] = cube_state[k]  # bottom -> back
            new_state[k] = cube_state[j]  # back -> top
            new_state[j] = cube_state[i]  # top -> front
            if column == 0:  # left side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while m < side_total:
                        new_row.append(cube_state[m])
                        m += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_clockwise(new_face)
                m = 0  # first index at left of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if column == cube_size - 1:  # right side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while n < side_total:
                        new_row.append(cube_state[n])
                        n += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_counterclockwise(new_face)
                n = side_total * 2  # first index at right of cube
                for value in rotated_face:
                    new_state[n] = value
                    n += 1

            i += cube_size
            j += cube_size
            k += cube_size
            l += cube_size
            column += 1

        # create new node with new_state
        if new_state not in used_states:
            new_node = Node()
            new_node.state = new_state
            new_node.parent = curr_node
            new_node.depth = curr_node.depth + 1
            curr_node.children.append(new_node)
            used_states.append(new_state)
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = side_total * 3  # first index at bottom of cube
        i += row
        j += row
        k += row
        l += row
        row += 1

    # move right front
    row = 1
    i = side_total * 5  # first index at front of cube
    j = side_total * 2  # first index at right of cube
    k = side_total * 4  # first index at back of cube
    l = 0  # first index at left of cube
    m = side_total  # first index at top of cube
    n = side_total * 3  # first index at bottom of cube
    while row <= cube_size:
        new_state = copy_list(cube_state)
        column = 0
        while column < cube_size:
            new_state[i] = cube_state[j]  # front -> right
            new_state[j] = cube_state[k]  # right -> back
            new_state[k] = cube_state[l]  # back -> left
            new_state[l] = cube_state[i]  # left -> front
            if row == 0:  # top side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while m < side_total:
                        new_row.append(cube_state[m])
                        m += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_counterclockwise(new_face)
                m = side_total  # first index at top of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if row == cube_size:  # bottom side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while n < side_total:
                        new_row.append(cube_state[n])
                        n += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_clockwise(new_face)
                n = side_total * 3  # first index at bottom of cube
                for value in rotated_face:
                    new_state[n] = value
                    n += 1

            i += 1
            j += 1
            k += 1
            l += 1
            column += 1

        # create new node with new_state
        if new_state not in used_states:
            new_node = Node()
            new_node.state = new_state
            new_node.parent = curr_node
            new_node.depth = curr_node.depth + 1
            curr_node.children.append(new_node)
            used_states.append(new_state)
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = side_total * 3  # first index at bottom of cube
        i += cube_size * row
        j += cube_size * row
        k += cube_size * row
        l += cube_size * row
        row += 1

    # move left front
    row = 1
    i = side_total * 5  # first index at front of cube
    j = side_total * 2  # first index at right of cube
    k = side_total * 4  # first index at back of cube
    l = 0  # first index at left of cube
    m = side_total  # first index at top of cube
    n = side_total * 3  # first index at bottom of cube
    while row <= cube_size:
        new_state = copy_list(cube_state)
        column = 0
        while column < cube_size:
            new_state[i] = cube_state[l]  # front -> left
            new_state[l] = cube_state[k]  # left -> back
            new_state[k] = cube_state[j]  # back -> right
            new_state[j] = cube_state[i]  # right -> front
            if row == 0:  # top side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while m < side_total:
                        new_row.append(cube_state[m])
                        m += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_clockwise(new_face)
                m = side_total  # first index at top of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if row == cube_size:  # bottom side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while n < side_total:
                        new_row.append(cube_state[n])
                        n += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_counterclockwise(new_face)
                n = side_total * 3  # first index at bottom of cube
                for value in rotated_face:
                    new_state[n] = value
                    n += 1

            i += 1
            j += 1
            k += 1
            l += 1
            column += 1

        # create new node with new_state
        if new_state not in used_states:
            new_node = Node()
            new_node.state = new_state
            new_node.parent = curr_node
            new_node.depth = curr_node.depth + 1
            curr_node.children.append(new_node)
            used_states.append(new_state)
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = side_total * 3  # first index at bottom of cube
        i += cube_size * row
        j += cube_size * row
        k += cube_size * row
        l += cube_size * row
        row += 1

    # move up left
    row = 1
    i = 0  # first index at left of cube
    j = side_total  # first index at top of cube
    k = side_total * 2  # first index at right of cube
    l = side_total * 3  # first index at bottom of cube
    m = side_total * 4  # first index at back of cube
    n = side_total * 5  # first index at front of cube
    while row <= cube_size:
        new_state = copy_list(cube_state)
        column = 0
        while column < cube_size:
            new_state[i] = cube_state[j]  # left -> top
            new_state[j] = cube_state[k]  # top -> right
            new_state[k] = cube_state[l]  # right -> bottom
            new_state[l] = cube_state[i]  # bottom -> left
            if column == 0:  # left side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while m < side_total:
                        new_row.append(cube_state[m])
                        m += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_counterclockwise(new_face)
                m = side_total * 4  # first index at back of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if column == cube_size - 1:  # right side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while n < side_total:
                        new_row.append(cube_state[n])
                        n += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_clockwise(new_face)
                n = side_total * 5  # first index at front of cube
                for value in rotated_face:
                    new_state[n] = value
                    n += 1

            i += cube_size
            j += cube_size
            k += cube_size
            l += cube_size
            column += 1

        # create new node with new_state if not already been created
        if new_state not in used_states:
            new_node = Node()
            new_node.state = new_state
            new_node.parent = curr_node
            new_node.depth = curr_node.depth + 1
            curr_node.children.append(new_node)
            used_states.append(new_state)
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = side_total * 3  # first index at bottom of cube
        i += row
        j += row
        k += row
        l += row
        row += 1

    # move down left
    row = 1
    i = 0  # first index at left of cube
    j = side_total  # first index at top of cube
    k = side_total * 2  # first index at right of cube
    l = side_total * 3  # first index at bottom of cube
    m = side_total * 4  # first index at back of cube
    n = side_total * 5  # first index at front of cube
    while row <= cube_size:
        new_state = copy_list(cube_state)
        column = 0
        while column < cube_size:
            new_state[i] = cube_state[l]  # left -> bottom
            new_state[l] = cube_state[k]  # bottom -> right
            new_state[k] = cube_state[j]  # right -> top
            new_state[j] = cube_state[i]  # top -> left
            if column == 0:  # left side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while m < side_total:
                        new_row.append(cube_state[m])
                        m += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_clockwise(new_face)
                m = side_total * 4  # first index at back of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if column == cube_size - 1:  # right side rotates
                z = 1
                new_face = list()
                while z <= cube_size:
                    new_row = list()
                    while n < side_total:
                        new_row.append(cube_state[n])
                        n += 1
                    new_face.append(new_row)
                    z += 1

                rotated_face = rotate_counterclockwise(new_face)
                n = side_total * 5  # first index at front of cube
                for value in rotated_face:
                    new_state[n] = value
                    n += 1

            i += cube_size
            j += cube_size
            k += cube_size
            l += cube_size
            column += 1

        # create new node with new_state if not already been created
        if new_state not in used_states:
            new_node = Node()
            new_node.state = new_state
            new_node.parent = curr_node
            new_node.depth = curr_node.depth + 1
            curr_node.children.append(new_node)
            used_states.append(new_state)
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = side_total * 3  # first index at bottom of cube
        i += row
        j += row
        k += row
        l += row
        row += 1


def a_star():
    initial_state, cube_size = randomize_cube()
    node = Node()
    node.state = initial_state
    path_to_goal = list()
    closed = list()
    transplanted = list()
    path_to_goal.append(node)
    scope_changes = 0


# to be called at top level
def main():
    parent = Node()
    state, size = randomize_cube()
    parent.state = state
    process_moves(parent, size)
    for child in parent.children:
        for i in child.state:
            print i,
        print ''


# top level code
if __name__ == '__main__':
    main()
