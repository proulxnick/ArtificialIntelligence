import math


def copy_list(old_list):
    # used to copy contents of one list and create another list

    new_list = list()
    for i in old_list:
        new_list.append(i)

    return new_list


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


def move_1(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    new_state = list()

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
            new_state[k] = cube_state[j]  # top -> back
            new_state[l] = cube_state[k]  # back -> bottom
            new_state[i] = cube_state[l]  # bottom -> front
            if row == 1 and not rotation:  # left side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m + cube_size])
                    z += 2
                    m += 2

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
                    new_face.append(cube_state[n:n + cube_size])
                    z += 2
                    n += 2

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
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = side_total * 3  # first index at bottom of cube
        i += row
        j += row
        k += row
        l += row
        row += 1

    return new_state


def move_2(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    new_state = list()

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
            new_state[k] = cube_state[l]  # bottom -> back
            new_state[j] = cube_state[k]  # back -> top
            new_state[i] = cube_state[j]  # top -> front
            if row == 1 and not rotation:  # left side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m + cube_size])
                    z += 2
                    m += 2

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
                    new_face.append(cube_state[n:n + cube_size])
                    z += 2
                    n += 2

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
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = side_total * 3  # first index at bottom of cube
        i += row
        j += row
        k += row
        l += row
        row += 1

    return new_state


def move_3(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    new_state = list()

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
            new_state[k] = cube_state[j]  # right -> back
            new_state[l] = cube_state[k]  # back -> left
            new_state[i] = cube_state[l]  # left -> front
            if row == 1 and not rotation:  # top side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m + cube_size])
                    z += 2
                    m += 2

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
                    new_face.append(cube_state[n:n + cube_size])
                    z += 2
                    n += 2

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
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = side_total * 3  # first index at bottom of cube
        i += cube_size * row
        j += cube_size * row
        k += cube_size * row
        l += cube_size * row
        row += 1

    return new_state


def move_4(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    new_state = list()

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
            new_state[k] = cube_state[l]  # left -> back
            new_state[j] = cube_state[k]  # back -> right
            new_state[i] = cube_state[j]  # right -> front
            if row == 1 and not rotation:  # top side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m + cube_size])
                    z += 2
                    m += 2

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
                    new_face.append(cube_state[n:n + cube_size])
                    z += 2
                    n += 2

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
        i = side_total * 5  # first index at front of cube
        j = side_total  # first index at top of cube
        k = side_total * 4  # first index at back of cube
        l = 0  # first index at left of cube
        i += cube_size * row
        j += cube_size * row
        k += cube_size * row
        l += cube_size * row
        row += 1

    return new_state


def move_5(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    new_state = list()

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
            new_state[k] = cube_state[j]  # top -> right
            new_state[l] = cube_state[k]  # right -> bottom
            new_state[i] = cube_state[l]  # bottom -> left
            if row == 1 and not rotation:  # left side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m + cube_size])
                    z += 2
                    m += 2

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
                    new_face.append(cube_state[n:n + cube_size])
                    z += 2
                    n += 2

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
        i = 0  # first index at left of cube
        j = side_total  # first index at top of cube
        k = side_total * 2  # first index at right of cube
        l = side_total * 3  # first index at bottom of cube
        i += row
        j += row
        k += row
        l += row
        row += 1

    return new_state


def move_6(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    new_state = list()

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
            new_state[k] = cube_state[l]  # bottom -> right
            new_state[j] = cube_state[k]  # right -> top
            new_state[i] = cube_state[j]  # top -> left
            if row == 1 and not rotation:  # left side rotates
                rotation = True
                z = 0
                new_face = list()
                while z < side_total:
                    new_face.append(cube_state[m:m + cube_size])
                    z += 2
                    m += 2

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
                    new_face.append(cube_state[n:n + cube_size])
                    z += 2
                    n += 2

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
        i = 0  # first index at left of cube
        j = side_total  # first index at top of cube
        k = side_total * 2  # first index at right of cube
        l = side_total * 3  # first index at bottom of cube
        i += row
        j += row
        k += row
        l += row
        row += 1

    return new_state
