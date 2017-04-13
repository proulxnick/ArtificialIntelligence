import random
import math

from index_config import shuffle_moves


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
                    and not tile.value == 1:
                complete = False
                break
            elif face_size * 2 >= i > face_size \
                    and not tile.value == 2:
                complete = False
                break
            elif face_size * 3 >= i > face_size * 2 \
                    and not tile.value == 3:
                complete = False
                break
            elif face_size * 4 >= i > face_size * 3 \
                    and not tile.value == 4:
                complete = False
                break
            elif face_size * 5 >= i > face_size * 4 \
                    and not tile.value == 5:
                complete = False
                break
            elif len(state) >= i > face_size * 5 \
                    and not tile.value == 6:
                complete = False
                break
            i += 1

        return complete


class Tile:

    def __init__(self, value):
        self.value = value
        self.position = None  # home index
        self.current = None  # current index
        self.column = None  # current column
        self.row = None  # current row


def copy_list(old_list):
    # used to copy contents of one list and create another list

    new_list = list()
    for i in old_list:
        new_list.append(i)

    return new_list


def cubie_distance(node, cube_size):
    x_axis_members = list()
    x = 1
    while x <= cube_size:
        x_axis_members.append([])

    y_axis_members = list()
    y = 1
    while y <= cube_size:
        y_axis_members.append([])

    # populate the face_members (z-axis finder)
    face_members = [[], [], [], [], [], []]
    face_members[0] = node.state[:cube_size]
    face_members[1] = node.state[cube_size:cube_size*2]
    face_members[2] = node.state[cube_size * 2:cube_size * 3]
    face_members[3] = node.state[cube_size * 3:cube_size * 4]
    face_members[4] = node.state[cube_size * 4:cube_size * 5]
    face_members[5] = node.state[cube_size * 5:]

    # populate x_members, y_members
    i = 0
    j = 0  # x boundary
    k = 0  # y boundary
    while i < len(node.state):
        for tile in node.state:
            x_axis_members[j].append(tile)
            y_axis_members[k].append(tile)


def out_of_place(node):
    # heuristic to find number of nodes out of goal state positioning
    i = 1
    count = 0
    face_size = len(node.state) / 6
    for tile in node.state:
        if i <= face_size \
           and not tile.value == 1:
            count += 1
        elif face_size * 2 >= i > face_size \
                and not tile.value == 2:
            count += 1
        elif face_size * 3 >= i > face_size * 2 \
                and not tile.value == 3:
            count += 1
        elif face_size * 4 >= i > face_size * 3 \
                and not tile.value == 4:
            count += 1
        elif face_size * 5 >= i > face_size * 4 \
                and not tile.value == 5:
            count += 1
        elif len(node.state) >= i > face_size * 5 \
                and not tile.value == 6:
            count += 1
        i += 1

    return count


def shuffle_cube(state, size):
    count = 1
    state = state
    while count <= 1:
        move_choice = random.randrange(1, 7)
        if move_choice == 1:
            state = shuffle_moves.move_1(state, size)
        elif move_choice == 2:
            state = shuffle_moves.move_2(state, size)
        elif move_choice == 3:
            state = shuffle_moves.move_3(state, size)
        elif move_choice == 4:
            state = shuffle_moves.move_4(state, size)
        elif move_choice == 5:
            state = shuffle_moves.move_5(state, size)
        elif move_choice == 6:
            state = shuffle_moves.move_6(state, size)
        count += 1

    return state


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
            tile = Tile(i)
            initial_state.append(tile)
            count2 += 1
        count1 += 1
        count2 = 0
        i += 1

    index = 0
    for tile in initial_state:
        tile.position = index
        index += 1

    initial_state = shuffle_cube(initial_state, size)  # randomize the order of the cube

    return initial_state, size


def rotate_counterclockwise(face):
    new_face = list()

    face = zip(*face)[::-1]
    for row in face:
        for value in row:
            new_face.append(value)

    cube_size = len(new_face) / 6
    degree = int(math.sqrt(cube_size))
    row = 1
    index = 0
    while row <= degree:
        column = 1
        while column <= degree:
            new_face[index].current = index
            new_face[index].column = column
            new_face[index].row = row
            index += 1
            column += 1
        row += 1

    return new_face


def rotate_clockwise(face):
    new_face = list()

    face = zip(*face[::-1])
    for row in face:
        for value in row:
            new_face.append(value)

    cube_size = len(new_face) / 6
    degree = int(math.sqrt(cube_size))
    row = 1
    index = 0
    while row <= degree:
        column = 1
        while column <= degree:
            new_face[index].current = index
            new_face[index].column = column
            new_face[index].row = row
            index += 1
            column += 1
        row += 1

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
        rotation = False
        while column < cube_size:
            new_state[j] = cube_state[i]  # front -> top
            new_state[j].current = j
            new_state[j].column = row
            new_state[j].row = column + 1

            new_state[k] = cube_state[j]  # top -> back
            new_state[k].current = k
            new_state[k].column = row
            new_state[k].row = column + 1

            new_state[l] = cube_state[k]  # back -> bottom
            new_state[l].current = l
            new_state[l].column = row
            new_state[l].row = column + 1

            new_state[i] = cube_state[l]  # bottom -> front
            new_state[i].current = j
            new_state[i].column = row
            new_state[i].row = column + 1

            if row == 1 and not rotation:  # left side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m+cube_size])
                    z += cube_size
                    m += cube_size

                rotated_face = rotate_counterclockwise(new_face)
                m = 0  # first index at left of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if row == cube_size and not rotation:  # right side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[n:n+cube_size])
                    z += cube_size
                    n += cube_size

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
        rotation = False
        while column < cube_size:
            new_state[l] = cube_state[i]  # front -> bottom
            new_state[l].current = l
            new_state[l].column = row
            new_state[l].row = column + 1

            new_state[k] = cube_state[l]  # bottom -> back
            new_state[k].current = l
            new_state[k].column = row
            new_state[k].row = column + 1

            new_state[j] = cube_state[k]  # back -> top
            new_state[j].current = j
            new_state[j].column = row
            new_state[j].row = column + 1

            new_state[i] = cube_state[j]  # top -> front
            new_state[i].current = i
            new_state[i].column = row
            new_state[i].row = column + 1

            if row == 1 and not rotation:  # left side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m+cube_size])
                    z += cube_size
                    m += cube_size

                rotated_face = rotate_clockwise(new_face)
                m = 0  # first index at left of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if row == cube_size and not rotation:  # right side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[n:n+cube_size])
                    z += cube_size
                    n += cube_size

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
        rotation = False
        while column < cube_size:
            new_state[j] = cube_state[i]  # front -> right
            new_state[j].current = j
            new_state[j].column = column + 1
            new_state[j].row = row

            new_state[k] = cube_state[j]  # right -> back
            new_state[k].current = k
            new_state[k].column = column + 1
            new_state[k].row = row

            new_state[l] = cube_state[k]  # back -> left
            new_state[l].current = l
            new_state[l].column = column + 1
            new_state[l].row = row

            new_state[i] = cube_state[l]  # left -> front
            new_state[i].current = i
            new_state[i].column = column + 1
            new_state[i].row = row

            if row == 1 and not rotation:  # top side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m+cube_size])
                    z += cube_size
                    m += cube_size

                rotated_face = rotate_counterclockwise(new_face)
                m = side_total  # first index at top of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if row == cube_size and not rotation:  # bottom side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[n:n+cube_size])
                    z += cube_size
                    n += cube_size

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
        rotation = False
        while column < cube_size:
            new_state[l] = cube_state[i]  # front -> left
            new_state[l].current = l
            new_state[l].column = column + 1
            new_state[l].row = row

            new_state[k] = cube_state[l]  # left -> back
            new_state[k].current = k
            new_state[k].column = column + 1
            new_state[k].row = row

            new_state[j] = cube_state[k]  # back -> right
            new_state[j].current = j
            new_state[j].column = column + 1
            new_state[j].row = row

            new_state[i] = cube_state[j]  # right -> front
            new_state[i].current = i
            new_state[i].column = column + 1
            new_state[i].row = row

            if row == 1 and not rotation:  # top side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m+cube_size])
                    z += cube_size
                    m += cube_size

                rotated_face = rotate_clockwise(new_face)
                m = side_total  # first index at top of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if row == cube_size and not rotation:  # bottom side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[n:n+cube_size])
                    z += cube_size
                    n += cube_size

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
        rotation = False
        while column < cube_size:
            new_state[j] = cube_state[i]  # left -> top
            new_state[j].current = j
            new_state[j].column = row
            new_state[j].row = column + 1

            new_state[k] = cube_state[j]  # top -> right
            new_state[k].current = k
            new_state[k].column = row
            new_state[k].row = column + 1

            new_state[l] = cube_state[k]  # right -> bottom
            new_state[l].current = l
            new_state[l].column = row
            new_state[l].row = column + 1

            new_state[i] = cube_state[l]  # bottom -> left
            new_state[i].current = i
            new_state[i].column = row
            new_state[i].row = column + 1

            if row == 1 and not rotation:  # left side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m+cube_size])
                    z += cube_size
                    m += cube_size

                rotated_face = rotate_counterclockwise(new_face)
                m = side_total * 4  # first index at back of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if row == cube_size and not rotation:  # right side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[n:n+cube_size])
                    z += cube_size
                    n += cube_size

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
        i = 0  # first index at left of cube
        j = side_total  # first index at top of cube
        k = side_total * 2  # first index at right of cube
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
        rotation = False
        while column < cube_size:
            new_state[l] = cube_state[i]  # left -> bottom
            new_state[l].current = l
            new_state[l].column = row
            new_state[l].row = column + 1

            new_state[k] = cube_state[l]  # bottom -> right
            new_state[k].current = k
            new_state[k].column = row
            new_state[k].row = column + 1

            new_state[j] = cube_state[k]  # right -> top
            new_state[j].current = j
            new_state[j].column = row
            new_state[j].row = column + 1

            new_state[i] = cube_state[j]  # top -> left
            new_state[i].current = i
            new_state[i].column = row
            new_state[i].row = column + 1

            if row == 1 and not rotation:  # left side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m+cube_size])
                    z += cube_size
                    m += cube_size

                rotated_face = rotate_clockwise(new_face)
                m = side_total * 4  # first index at back of cube
                for value in rotated_face:
                    new_state[m] = value
                    m += 1

            if row == cube_size and not rotation:  # right side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[n:n+cube_size])
                    z += cube_size
                    n += cube_size

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
        i = 0  # first index at left of cube
        j = side_total  # first index at top of cube
        k = side_total * 2  # first index at right of cube
        l = side_total * 3  # first index at bottom of cube
        i += row
        j += row
        k += row
        l += row
        row += 1

    return curr_node, cube_size


def path_exists(path_list, new_node):
    # this is a method to check if the state of the given node exists in the given path
    is_old_state = False

    for node in path_list:
        if new_node.state == node.state:
            is_old_state = True

    return is_old_state


def a_star():
    initial_state, cube_size = randomize_cube()
    node = Node()
    node.state = initial_state
    path_to_goal = list()
    path_to_goal.append(node)
    closed = list()
    transplanted = list()
    scope_changes = 0

    while not node.is_at_goal(node.state):
        # initialize the curr node's children + get their states
        node, cube_size = process_moves(node, cube_size)

        cheapest = None
        curr_node = Node()
        for each_node in node.children:
            if not path_exists(path_to_goal, each_node):
                heuristic = out_of_place(each_node)
                if cheapest is None \
                        or heuristic < cheapest:
                    cheapest = heuristic
                    curr_node = each_node  # current node now has cheapest run time at it's depth
                    if cheapest == 0:  # at goal
                        break

        for each_node in node.children:
            cost = out_of_place(each_node)
            if not each_node.state == curr_node.state:
                each_node.heuristic_value = cost
                closed.append(each_node)  # only append if the current node is not in the closed list
            else:
                curr_node.heuristic_value = cost

        transplant = False  # to check if a node's children were transplanted for change of scope
        if path_exists(closed, curr_node):
            for closed_node in closed:
                if closed_node.state == curr_node.state \
                        and closed_node.heuristic_value <= curr_node.heuristic_value \
                        and closed_node.depth < curr_node.depth \
                        and closed_node.state not in transplanted \
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
    return path_to_goal, cube_size


def print_cube_state(state, cube_size):
    #  print back side
    x = 0
    z = 1
    while x < len(state):
        print state[x].value,
        if z == math.pow(cube_size, 2):
            print ' ',
            z = 0
        z += 1
        x += 1

    print '\n\n'


# to be called at top level
def main():
    path, size = a_star()
    for child in path:
        print_cube_state(child.state, size)


# top level code
if __name__ == '__main__':
    main()
