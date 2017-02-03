class BridgeCrossException(Exception):

    def __init__(self, message):
        self.message = message


class Runner:

    def __init__(self, run_time):
        self.run_time = run_time


class State:

    def __init__(self, left_num, torch, right_num, run_time):
        self.runners_left = left_num
        self.torch = torch
        self.runners_right = right_num
        self.run_time = run_time

    def is_at_goal(self):
        if self.runners_left == 0 \
           and self.torch == 'Right' \
           and self.runners_right > 0:
            return True
        else:
            return False

    def is_valid_cross(self):
        if 0 <= self.runners_left <= 6 \
           and 0 <= self.runners_right <= 6:
            return True
        else:
            return False


class Node:

    def __init__(self):
        self.state = None
        self.parent = None
        self.depth = 0
        self.children = list()  # to be used to create possible chile nodes dynamically and append to list


# only hard coded for testing
def initiate_runners():

    left_side = list()
    right_side = list()
    torch = 'Left'

    # define the runners
    r1 = Runner(4)
    r2 = Runner(6)
    r3 = Runner(8)
    r4 = Runner(10)
    r5 = Runner(12)
    r6 = Runner(14)

    left_side.append(r1)
    left_side.append(r2)
    left_side.append(r3)
    left_side.append(r4)
    left_side.append(r5)
    left_side.append(r6)

    # initialize the root state and create a new root node with that state
    left_num = len(left_side)
    right_num = len(right_side)
    initial_state = State(left_num, torch, right_num, 0)
    node = Node()
    node.depth = 0
    node.parent = None
    node.state = initial_state
    run_time = node.state.run_time

    return left_side, torch, right_side, node, run_time


def path_exists(path_list, new_node):
    is_old_state = False

    for node in path_list:
        if new_node.state.runners_left == node.state.runners_left \
           and new_node.state.runners_right == node.state.runners_right \
           and new_node.state.torch == node.state.torch:
            is_old_state = True
            break

    return is_old_state


def successor_processing(state, old_node, left_runners, right_runners):
    frontier = []

    if state.is_at_goal():
        return 'Already at goal!'

    elif state.torch == 'Left':
        if len(left_runners) > 1:
            while len(left_runners) > 1:
                # move 2 runners at a time across the bridge
                new_state = State(state.runners_left - 2, 'Right', state.runners_right + 2,
                                  max(left_runners[0].run_time, left_runners[1].run_time))
                if new_state.is_valid_cross():
                    new_node = Node()
                    new_node.state = new_state
                    new_node.parent = old_node
                    new_node.depth = old_node.depth + 1
                    old_node.children.append(new_node)
                    frontier.append(new_node)
                    right_runners.append(left_runners[1])
                    right_runners.append(left_runners[0])
                    left_runners.remove(left_runners[1])
                    left_runners.remove(left_runners[0])

        if len(left_runners) == 1:
            # maybe for some reason there is less than 2 people and need to bring only one to right
            new_state = State(state.runners_left - 1, 'Right', state.runners_right + 1, left_runners[0].run_time)
            if new_state.is_valid_cross():
                new_node = Node
                new_node.state = new_state
                new_node.parent = old_node
                new_node.depth = old_node.depth + 1
                old_node.children.append(new_node)
                frontier.append(new_node)
                right_runners.append(left_runners[0])
                left_runners.remove(left_runners[0])

        return old_node, left_runners, right_runners

    elif state.torch == 'Right':
        for runner in right_runners:
            new_state = State(state.runners_left + 1, 'Left', state.runners_right - 1, runner.run_time)
            if new_state.is_valid_cross():
                new_node = Node()
                new_node.state = new_state
                new_node.parent = old_node
                new_node.depth = old_node.depth + 1
                old_node.children.append(new_node)
                frontier.append(new_node)
                left_runners.append(right_runners[0])
                right_runners.remove(right_runners[0])

        return old_node, left_runners, right_runners

    else:
        raise BridgeCrossException('Invalid torch placement')


def breadth_first():
    # initialize the root state and create a new root node with that state
    left_side, torch, right_side, node, run_time = initiate_runners()

    path_to_goal = list()
    path_to_goal.append(node)

    while not node.state.is_at_goal():
        node, left_side, right_side = successor_processing(node.state,
                                                           node,
                                                           left_side,
                                                           right_side)
        cheapest_run_time = 0
        cheapest_node = Node()
        for each_node in node.children:
            if not path_exists(path_to_goal, each_node):
                if cheapest_run_time == 0 \
                   or each_node.state.run_time < cheapest_run_time:
                    cheapest_run_time = each_node.state.run_time
                    cheapest_node = each_node
        path_to_goal.append(cheapest_node)
        run_time += cheapest_node.state.run_time
        node = cheapest_node

    return path_to_goal, run_time


def depth_first():
    # initialize the root state and create a new root node with that state
    left_side, torch, right_side, node, run_time = initiate_runners()

    path_to_goal = list()
    path_to_goal.append(node)

    stack = list()

    while not node.state.is_at_goal():
        node, left_side, right_side = successor_processing(node.state,
                                                           node,
                                                           left_side,
                                                           right_side)
        for each_node in node.children:
            stack.append(each_node)

        new_node = stack.pop()
        if not path_exists(path_to_goal, new_node) \
           and new_node.state.is_valid_cross():
            path_to_goal.append(new_node)
            run_time += new_node.state.run_time
            node = new_node

    return path_to_goal, run_time


def print_path():
    # path, run_time = breadth_first()
    path, run_time = depth_first()
    i = 0
    for node in path:
        print 'Move: ' + str(i)
        print str(node.state.runners_left) + ',  ' + node.state.torch + ',  ' + str(node.state.runners_right)
        print 'Crossing Time: ' + str(node.state.run_time) + '\n'
        i += 1

    print 'Done!'
    print 'Total Time Elapsed: ' + str(run_time)


def main():
    print_path()


if __name__ == '__main__':
    main()
