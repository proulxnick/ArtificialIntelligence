import math
import random


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
    column = random.randrange(0, cube_size)

    # move up front
    i = (side_total * 5) + column  # first index at front of cube
    j = side_total + column  # first index at top of cube
    k = (side_total * 4) + column  # first index at back of cube
    l = (side_total * 3) + column  # first index at bottom of cube
    m = 0  # first index at left of cube
    n = side_total * 2  # first index at right of cube
    new_state = copy_list(cube_state)
    rotation = False
    limit = 0
    while limit < cube_size:
        new_state[j] = cube_state[i]  # front -> top
        new_state[j].current = j
        new_state[j].column = column + 1
        new_state[j].row = limit + 1

        new_state[k] = cube_state[j]  # top -> back
        new_state[k].current = k
        new_state[k].column = column + 1
        new_state[k].row = limit + 1

        new_state[l] = cube_state[k]  # back -> bottom
        new_state[l].current = l
        new_state[l].column = column + 1
        new_state[l].row = limit + 1

        new_state[i] = cube_state[l]  # bottom -> front
        new_state[i].current = j
        new_state[i].column = column + 1
        new_state[i].row = limit + 1

        if column == 0 and not rotation:  # left side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[m:m + cube_size])
                z += cube_size
                m += cube_size

            rotated_face = rotate_counterclockwise(new_face)
            m = 0  # first index at left of cube
            for value in rotated_face:
                new_state[m] = value
                m += 1

        if column == cube_size and not rotation:  # right side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[n:n + cube_size])
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
        limit += 1

    return new_state


def move_2(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    column = random.randrange(0, cube_size)

    # move up front
    i = (side_total * 5) + column  # first index at front of cube
    j = side_total + column  # first index at top of cube
    k = (side_total * 4) + column  # first index at back of cube
    l = (side_total * 3) + column  # first index at bottom of cube
    m = 0  # first index at left of cube
    n = side_total * 2  # first index at right of cube
    new_state = copy_list(cube_state)
    rotation = False
    limit = 0
    while limit < cube_size:
        new_state[l] = cube_state[i]  # front -> bottom
        new_state[l].current = l
        new_state[l].column = column + 1
        new_state[l].row = limit + 1

        new_state[k] = cube_state[l]  # bottom -> back
        new_state[k].current = l
        new_state[k].column = column + 1
        new_state[k].row = limit + 1

        new_state[j] = cube_state[k]  # back -> top
        new_state[j].current = j
        new_state[j].column = column + 1
        new_state[j].row = limit + 1

        new_state[i] = cube_state[j]  # top -> front
        new_state[i].current = i
        new_state[i].column = column + 1
        new_state[i].row = limit + 1

        if column == 0 and not rotation:  # left side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[m:m + cube_size])
                z += cube_size
                m += cube_size

            rotated_face = rotate_clockwise(new_face)
            m = 0  # first index at left of cube
            for value in rotated_face:
                new_state[m] = value
                m += 1

        if column == cube_size and not rotation:  # right side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[n:n + cube_size])
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
        limit += 1

    return new_state


def move_3(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    column = random.randrange(0, cube_size)

    # move right front
    i = (side_total * 5) + (column * cube_size)  # first index at front of cube
    j = (side_total * 2) + (column * cube_size)  # first index at right of cube
    k = (side_total * 4) + (column * cube_size)  # first index at back of cube
    l = column * cube_size  # first index at left of cube
    m = side_total  # first index at top of cube
    n = side_total * 3  # first index at bottom of cube
    limit = 0
    new_state = copy_list(cube_state)
    rotation = False
    while limit < cube_size:
        new_state[j] = cube_state[i]  # front -> right
        new_state[j].current = j
        new_state[j].column = limit + 1
        new_state[j].row = column + 1

        new_state[k] = cube_state[j]  # right -> back
        new_state[k].current = k
        new_state[k].column = limit + 1
        new_state[k].row = column + 1

        new_state[l] = cube_state[k]  # back -> left
        new_state[l].current = l
        new_state[l].column = limit + 1
        new_state[l].row = column + 1

        new_state[i] = cube_state[l]  # left -> front
        new_state[i].current = i
        new_state[i].column = limit + 1
        new_state[i].row = column + 1

        if column == 0 and not rotation:  # top side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[m:m + cube_size])
                z += cube_size
                m += cube_size

            rotated_face = rotate_counterclockwise(new_face)
            m = side_total  # first index at top of cube
            for value in rotated_face:
                new_state[m] = value
                m += 1

        if column == cube_size and not rotation:  # bottom side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[n:n + cube_size])
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
        limit += 1

    return new_state


def move_4(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    column = random.randrange(0, cube_size)

    # move right front
    i = (side_total * 5) + (column * cube_size)  # first index at front of cube
    j = (side_total * 2) + (column * cube_size)  # first index at right of cube
    k = (side_total * 4) + (column * cube_size)  # first index at back of cube
    l = column * cube_size  # first index at left of cube
    m = side_total  # first index at top of cube
    n = side_total * 3  # first index at bottom of cube
    limit = 0
    new_state = copy_list(cube_state)
    rotation = False
    while limit < cube_size:
        new_state[l] = cube_state[i]  # front -> left
        new_state[l].current = l
        new_state[l].column = limit + 1
        new_state[l].row = column + 1

        new_state[k] = cube_state[l]  # left -> back
        new_state[k].current = k
        new_state[k].column = limit + 1
        new_state[k].row = column + 1

        new_state[j] = cube_state[k]  # back -> right
        new_state[j].current = j
        new_state[j].column = limit + 1
        new_state[j].row = column + 1

        new_state[i] = cube_state[j]  # right -> front
        new_state[i].current = i
        new_state[i].column = limit + 1
        new_state[i].row = column + 1

        if column == 0 and not rotation:  # top side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[m:m + cube_size])
                z += cube_size
                m += cube_size

            rotated_face = rotate_clockwise(new_face)
            m = side_total  # first index at top of cube
            for value in rotated_face:
                new_state[m] = value
                m += 1

        if column == cube_size and not rotation:  # bottom side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[n:n + cube_size])
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
        limit += 1

    return new_state


def move_5(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    column = random.randrange(0, cube_size)

    # move up left
    i = column  # first index at left of cube
    j = side_total + column  # first index at top of cube
    k = (side_total * 2) + column  # first index at right of cube
    l = (side_total * 3) + column  # first index at bottom of cube
    m = side_total * 4  # first index at back of cube
    n = side_total * 5  # first index at front of cube
    new_state = copy_list(cube_state)
    limit = 0
    rotation = False
    while limit < cube_size:
        new_state[j] = cube_state[i]  # left -> top
        new_state[j].current = j
        new_state[j].column = column + 1
        new_state[j].row = limit + 1

        new_state[k] = cube_state[j]  # top -> right
        new_state[k].current = k
        new_state[k].column = column + 1
        new_state[k].row = limit + 1

        new_state[l] = cube_state[k]  # right -> bottom
        new_state[l].current = l
        new_state[l].column = column + 1
        new_state[l].row = limit + 1

        new_state[i] = cube_state[l]  # bottom -> left
        new_state[i].current = i
        new_state[i].column = column + 1
        new_state[i].row = limit + 1

        if column == 0 and not rotation:  # left side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[m:m + cube_size])
                z += cube_size
                m += cube_size

            rotated_face = rotate_counterclockwise(new_face)
            m = side_total * 4  # first index at back of cube
            for value in rotated_face:
                new_state[m] = value
                m += 1

        if column == cube_size and not rotation:  # right side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[n:n + cube_size])
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
        limit += 1

    return new_state


def move_6(cube_state, cube_size):
    side_total = int(math.pow(cube_size, 2))
    column = random.randrange(0, cube_size)

    # move up left
    i = column  # first index at left of cube
    j = side_total + column  # first index at top of cube
    k = (side_total * 2) + column  # first index at right of cube
    l = (side_total * 3) + column  # first index at bottom of cube
    m = side_total * 4  # first index at back of cube
    n = side_total * 5  # first index at front of cube
    new_state = copy_list(cube_state)
    limit = 0
    rotation = False
    while limit < cube_size:
        new_state[l] = cube_state[i]  # left -> bottom
        new_state[l].current = l
        new_state[l].column = column + 1
        new_state[l].row = limit + 1

        new_state[k] = cube_state[l]  # bottom -> right
        new_state[k].current = k
        new_state[k].column = column + 1
        new_state[k].row = limit + 1

        new_state[j] = cube_state[k]  # right -> top
        new_state[j].current = j
        new_state[j].column = column + 1
        new_state[j].row = limit + 1

        new_state[i] = cube_state[j]  # top -> left
        new_state[i].current = i
        new_state[i].column = column + 1
        new_state[i].row = limit + 1

        if column == 0 and not rotation:  # left side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[m:m + cube_size])
                z += cube_size
                m += cube_size

            rotated_face = rotate_clockwise(new_face)
            m = side_total * 4  # first index at back of cube
            for value in rotated_face:
                new_state[m] = value
                m += 1

        if column == cube_size and not rotation:  # right side rotates
            rotation = True
            z = 0
            new_face = list()
            while z < side_total:
                new_face.append(cube_state[n:n + cube_size])
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
        limit += 1

    return new_state
