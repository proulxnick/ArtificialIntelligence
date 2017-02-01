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
           and self.torch == 'Right':
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
        self.children = []  # to be used to create possible chile nodes dynamically and append to list


# only hard coded for testing
def initiate_crossing():

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

    return left_side, torch, right_side


def process_crossing(state, old_node, left_runners, right_runners):
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
            new_state = State(state.runners_left - 1, 'Right', state.runners_right + 1, runner.run_time)
            if new_state.is_valid_cross():
                new_node = Node
                new_node.state = new_state
                new_node.parent = old_node
                new_node.depth = old_node.depth + 1
                old_node.children.append(new_node)
                frontier.append(new_node)

        return frontier, left_runners, right_runners

    elif state.torch == 'Right':
        for runner in right_runners:
            new_state = State(state.runners_left + 1, 'Left', state.runners_right - 1, runner.run_time)
            if new_state.is_valid_cross():
                new_node = Node
                new_node.state = new_state
                new_node.parent = old_node
                new_node.depth = old_node.depth + 1
                old_node.children.append(new_node)
                frontier.append(new_node)

        return frontier, left_runners, right_runners

    else:
        raise BridgeCrossException('Invalid torch placement')


def breadth_first():
    # initialize the root state and create a new root node with that state
    left_side, torch, right_side = initiate_crossing()
    left_runners = len(left_side)
    right_runners = len(right_side)
    initial_state = State(left_runners, torch, right_runners, 0)
    root_node = Node()
    root_node.depth = 0
    root_node.parent = None
    root_node.state = initial_state

    fronteir, left_runners, right_runners = process_crossing(initial_state, root_node, left_side, right_side)


def main():
    breadth_first()


if __name__ == '__main__':
    main()
